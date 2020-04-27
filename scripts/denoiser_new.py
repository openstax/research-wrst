# Implements a 3PL IRT model
# TODO: Set a type variable for the IRT for 1PL, 2PL, and 3PL models
# 1PL can have an additional routine for sampling beta more efficiently
# Fit method will call whatever appropriate fit construct given the type

import numpy as np
from scipy.stats import norm
from time import time

default_params = {'mu_theta': 0, 'sigma_theta': 1,
                  'mu_mu': 0, 'sigma_mu': 1,
                  'alpha_alpha': 1, 'beta_alpha': 3,
                  'alpha_gamma': 1, 'beta_gamma': 10,
                  'T': 10000, 'burnin': 1000, 'thinning': 1}

class WRSTDenoiser(object):
    def __init__(self, **kwargs):
        self.__dict__ = default_params
        allowed_keys = default_params.keys()
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def truncnorm(self, a_t, b_t, mu_t, sigma_t):
        # Create the mask matrix for dealing with missing data (nans)
        C = np.isnan(a_t) + np.isnan(b_t) + np.isnan(mu_t) + np.isnan(sigma_t)
        idx = np.where(~C)
        a = a_t[idx]
        b = b_t[idx]
        mu = mu_t[idx]
        sigma = sigma_t[idx]
        O = np.nan * np.zeros(C.shape)

        N = np.prod(np.array(mu).shape)
        alpha = (a - mu) / sigma
        beta = (b - mu) / sigma
        Phi_alpha = norm.cdf(alpha)
        Phi_beta = norm.cdf(beta)
        U = np.random.rand(N)
        out = norm.ppf(Phi_alpha + U * (Phi_beta - Phi_alpha)) * sigma + mu

        # If any elements in out are nan . . . if so set to mu
        nan_idx = np.where(np.isnan(out))
        out[nan_idx] = mu[nan_idx]
        O[idx] = out

        # Return the final result
        return O

    def setup_mcmc_samples(self):
        # Set up the dataframes for saving off samples
        N = self.N
        Q = self.Q

        samples_to_save = int((self.T - self.burnin) / self.thinning)
        self.LL = np.zeros(self.T)
        self.W_mcmc = np.zeros((N, Q))
        self.theta_mcmc = np.zeros((N, samples_to_save))
        self.mu_mcmc = np.zeros((Q, samples_to_save))
        self.alpha_mcmc = np.zeros((Q, samples_to_save))
        self.C_mcmc = np.zeros((Q, samples_to_save))
        self.gamma_mcmc = np.zeros((Q, samples_to_save))

    def save_samples(self, W, Z, theta, alpha, mu, C, gamma, t):
        idx = int((t - self.burnin) / self.thinning)
        self.W_mcmc = self.W_mcmc + 1.0 * W / ((self.T - self.burnin) / self.thinning)
        self.theta_mcmc[:, idx:idx + 1] = theta
        self.mu_mcmc[:, idx:idx + 1] = mu
        self.alpha_mcmc[:, idx:idx + 1] = alpha
        self.gamma_mcmc[:, idx:idx + 1] = gamma
        C.shape = (len(C), 1)
        self.C_mcmc[:, idx:idx + 1] = C

    # def sample_W(self, Y, eta, gamma):
    #
    #     gamma_temp = np.tile(gamma.T, (self.N, 1))
    #     Phi = norm.cdf(eta)
    #     P = Y * Phi / (gamma_temp + (1 - gamma_temp) * Phi)
    #     W = 1.0 * (np.random.rand(*P.shape) < P)
    #     W[np.isnan(Y)] = np.nan
    #     return W

    def sample_Z(self, eta, W):
        # Configure the limits based on the values in W
        # eta is alpha*(theta-mu)
        A = np.zeros(W.shape)
        B = np.zeros(W.shape)
        Sigma = np.ones(W.shape)
        A[W == 0] = -np.inf
        B[W == 1] = np.inf
        Z = self.truncnorm(A, B, eta, Sigma)
        Z[np.isnan(W)] = np.nan
        return Z

    def sample_theta(self, Z, mu, alpha):
        alpha_matrix = np.tile(alpha.T, (self.N, 1))
        alpha_matrix[np.isnan(Z)] = np.nan
        Z_prime = Z + np.tile(mu.T, (self.N, 1))
        Z_prime = Z_prime * alpha_matrix
        S_alpha = np.nansum(alpha_matrix, axis=1, keepdims=True)
        mean = (np.nansum(Z_prime, axis=1, keepdims=True) / (S_alpha + 1 / (self.sigma_theta ** 2)))
        var = 1.0 / (1.0 / self.sigma_theta ** 2 + S_alpha)
        theta_out = np.sqrt(var) * np.random.randn(self.N, 1) + mean
        return theta_out

    def sample_mu(self, Z, theta, alpha):
        alpha_matrix = np.tile(alpha.T, (self.N, 1))
        alpha_matrix[np.isnan(Z)] = np.nan
        Z_prime = -1*(Z - np.tile(theta, (1, self.Q)))
        Z_prime = Z_prime * alpha_matrix
        S_alpha = np.nansum(alpha_matrix, axis=0, keepdims=True)
        mean = (np.nansum(Z_prime, axis=0, keepdims=True) / (S_alpha + 1 / (self.sigma_mu ** 2)))
        var = 1.0 / (1.0 / self.sigma_mu ** 2 + S_alpha)
        mu_out = np.sqrt(var) * np.random.randn(1, self.Q) + mean
        return mu_out.T

    def sample_alpha(self, Z, theta, mu):
        Zhat = Z + np.tile(mu.T, (self.N, 1)) - np.tile(theta, (1, self.Q))
        D2 = Zhat ** 2 / 2
        N_obs = np.sum(~np.isnan(Zhat), axis=0)
        alpha_hat = self.alpha_alpha + N_obs / 2
        beta_hat = self.beta_alpha + np.nansum(D2, axis=0)
        out = np.random.gamma(alpha_hat, 1/beta_hat, self.Q)
        out.shape = (self.Q, 1)
        return out


    def sample_C(self, Z, L):
        # For each task, aggregate the success probabilities and labels for each user
        # Assemble the dirichlet posterior and sample once per task
        P = norm.cdf(Z)
        P0 = 1 - P
        p_alpha = np.zeros((self.K, self.Q))
        for k in range(self.K):
            Pt = np.zeros(P.shape)
            Pt[L==k] = P[L==k]
            p_alpha[k, :] = np.sum(Pt, axis=0)

        # Sample a new distribution from the posterior dirichlet and select a new "correct" category
        p_alpha = p_alpha + np.ones(p_alpha.shape) / self.K
        p_temp = np.zeros(p_alpha.shape)
        C = np.zeros(self.Q)
        for qq in range(self.Q):
            p_temp[:, qq] = np.random.dirichlet(p_alpha[:, qq])
            C[qq] = np.random.choice(self.K, p=p_temp[:, qq])
        return C.astype(int)

    def sample_W(self, L, eta, C, gamma):
        # W=0 whenever L!=C
        # Otherwise, we have to way prob of guessing C vs knowing C
        P = norm.cdf(eta)
        # Pg = np.zeros(P.shape) # ugh this hurts make this suck less
        # for qq in range(self.Q):
        #     Pg[:, qq] = F[qq, C[qq]]
        Pg = np.tile(gamma.T, (self.N, 1))
        G = P / ((1-Pg)*P + Pg)
        W = 1.0 * (np.random.rand(self.N, self.Q) <= G)
        W[L != np.tile(C.T, (self.N, 1))] = 0
        W[np.isnan(L)] = np.nan
        return W

    def sample_gamma(self, L, C, W):
        Y = 1.0 * (L==np.tile(C, (self.N, 1)))
        Y[np.isnan(L)] = np.nan
        gamma = np.zeros((self.Q, 1))
        a = np.nansum(1-W, axis=0)
        b = np.nansum((1-W)*Y, axis=0)
        for gg in range(0, self.Q):
            gamma[gg] = np.random.beta(self.alpha_gamma + b[gg], self.beta_gamma - b[gg] + a[gg])
        return gamma


    def fit(self, data, theta_init=None, mu_init=None, alpha_init=None, W_init=None, C_init=None, gamma_init=None):
        self.data = data
        self.N, self.Q = data.shape
        self.K = int(np.nanmax(data) + 1)

        t_w = np.zeros(self.T)
        t_z = np.zeros(self.T)
        t_th = np.zeros(self.T)
        t_mu = np.zeros(self.T)
        t_a = np.zeros(self.T)
        t_cf = np.zeros(self.T)
        t_g = np.zeros(self.T)

        # Initialize model parameters parameters according to priors
        if (theta_init is None):
            theta = self.sigma_theta * np.random.randn(self.N, 1) + self.mu_theta
        else:
            theta = theta_init
        if (mu_init is None):
            mu = self.sigma_mu * np.random.randn(self.Q, 1) + self.mu_mu
        else:
            mu = mu_init
        if (alpha_init is None):
            alpha = np.random.gamma(self.alpha_alpha, 1 / self.beta_alpha, size=(self.Q, 1))
        else:
            alpha = alpha_init
        if (C_init is None):
            C = np.random.choice(self.K, size=(self.Q, 1))
        else:
            C = C_init
        if (gamma_init is None):
            gamma = np.random.beta(self.alpha_gamma, self.beta_gamma, size=(self.Q, 1))
        else:
            gamma = gamma_init
        if W_init is not None:
            W = W_init


        # Initialize the state variables
        self.setup_mcmc_samples()

        # Run the chain
        for t in range(0, self.T):
            if ((t + 1) % 1 == 0):
                print("Iter: " + str(t + 1))

            # Compute log liklihood
            # self.LL[t] = self.compute_LL(data, theta, alpha, beta, gamma)

            # Compute current value of eta = alpha*(theta - beta)
            alpha = np.ones((self.Q, 1))
            eta = np.tile(alpha.T, (self.N, 1)) * (np.tile(theta, (1, self.Q)) - np.tile(mu.T, (self.N, 1)))
            self.eta = eta

            # Sample W
            t1 = time()
            W = self.sample_W(data, eta, C, gamma)
            # W = W_init
            t_w[t] = time() - t1

            # Sample Z
            t1 = time()
            Z = self.sample_Z(eta, W)
            t_z[t] = time() - t1

            # Sample theta
            t1 = time()
            theta = self.sample_theta(Z, mu, alpha)
            t_th[t] = time() - t1

            # Sample mu
            t1 = time()
            mu = self.sample_mu(Z, theta, alpha)
            t_mu[t] = time() - t1

            # Sample alpha
            t1 = time()
            # alpha = self.sample_alpha(Z, theta, mu)
            t_a[t] = time() - t1

            # Sample C
            t1 = time()
            C = self.sample_C(Z, data)
            # C = C_init
            # F = F_init
            t_cf[t] = time() - t1

            # Sample gamma
            t1 = time()
            gamma = self.sample_gamma(data, C, W)
            # gamma = gamma_init
            t_g[t] = time() - t1

            # Save off values if t>burnin
            if (t >= self.burnin) & (((t - self.burnin) % self.thinning) == 0):
                self.save_samples(W, Z, theta, alpha, mu, C, gamma, t)
        self.t_w = t_w
        self.t_z = t_z
        self.t_th = t_th
        self.t_mu = t_mu
        self.t_a = t_th
        self.t_cf = t_cf
        self.t_g = t_g

    def compute_LL(self, data, theta, alpha, beta, gamma):

        D = data[~np.isnan(data)]

        eta = np.tile(alpha.T, (self.N, 1)) * np.tile(theta, (1, self.Q)) - np.tile(beta.T, (self.N, 1))
        gamma_temp = np.tile(gamma.T, (self.N, 1))
        P_pos = gamma_temp + (1 - gamma_temp) * norm.cdf(eta)
        P_neg = 1 - P_pos
        P_pos = P_pos[~np.isnan(data)]
        P_neg = P_neg[~np.isnan(data)]

        P = P_pos
        P[D == 0] = P_neg[D == 0]
        P = np.clip(P, 1e-3, 1 - 1e-3)

        return np.sum(-np.log(P))

    def generate_synthetic_data(self, N, Q, K, p_obs=1):
        # N participants responding to Q tasks, outcome is one of K discrete labels
        # Final matrices are N x Q

        # Generate the participant parameters
        theta = self.sigma_theta * np.random.randn(N, 1) + self.mu_theta

        # Generate the task parameters
        # Prior on C is dirichlet but we can just generate the label from a DU
        mu = self.sigma_mu * np.random.randn(Q, 1) + self.mu_mu
        # alpha = np.random.gamma(self.alpha_alpha, 1/self.beta_alpha, (Q, 1))
        alpha = np.ones((Q,1))
        C = np.random.choice(range(K), Q)
        gamma = np.random.beta(self.alpha_gamma, self.beta_gamma, size=(self.Q, 1))

        # Generate the remaining model parameters (prob correct, actual correctness)
        eta = np.tile(alpha.T, (N, 1)) * (np.tile(theta, (1, Q)) - np.tile(mu.T, (N, 1)))
        W = 1.0 * (np.random.rand(N, Q) < norm.cdf(eta))
        Gamma = np.tile(gamma.T, (N, 1))
        guess = np.random.rand(N, Q) < Gamma

        # Generate the label for each user/task pair
        # If user is correct, label is the correct one
        # If user in incorrect, label is drawn from Fq
        # Just draw everything from Fq and then replace where needed for simplicity
        C_mat = np.tile(C, (N, 1))
        L = np.random.choice(K, size=(N, Q))
        L[L==C_mat] = (L[L==C_mat]+1) % K # Enforces guesses not equal to right label
        L[W==1] = C_mat[W==1] #...unless W==1
        L[guess==1] = C_mat[guess==1] # or they guess right
        L = L.astype(float)

        # Sample L uniformly according to p_obs
        P_punc = np.random.rand(N, Q) < (1 - p_obs)
        L[P_punc] = np.nan
        return L, guess, W, gamma, C, theta, mu, alpha

