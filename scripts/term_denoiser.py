# Implements a 3PL IRT model
# TODO: Set a type variable for the IRT for 1PL, 2PL, and 3PL models
# 1PL can have an additional routine for sampling beta more efficiently
# Fit method will call whatever appropriate fit construct given the type

import numpy as np
from scipy.stats import norm
from time import time

# Brief model description:
# User observes a term t and has to decide if it is a key term or not
# User has a bias and variance that affects this observation

# Model equations:
# mu_i ~ N(mu_mu, tau_mu), tau_i ~ Gamma(alpha_tau, beta_tau) [user]
# t_j ~ N(mu_t, tau_t) [term]
# T_ij ~ N(t_j + mu_i, tau_i) [observation by user i of term j]
# Y_ij = (T_ij > 0) [observation in data, equiv to probit model on T_ij]

default_params = {'mu_mu': 0, 'tau_mu': .2,
                  'mu_t': 0, 'tau_t': .2,
                  'alpha_tau': 1, 'beta_tau': 1,
                  'T': 10000, 'burnin': 1000, 'thinning': 1}

class TermDenoiser(object):
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
        self.T_mcmc = np.zeros((N, Q, samples_to_save))
        self.mu_mcmc = np.zeros((N, samples_to_save))
        self.t_mcmc = np.zeros((Q, samples_to_save))
        self.tau_mcmc = np.zeros((N, samples_to_save))

    def save_samples(self, T, mu, tau, t, iteration):
        idx = int((iteration - self.burnin) / self.thinning)
        self.T_mcmc[:, :, idx:idx + 1] = T
        self.mu_mcmc[:, idx:idx + 1] = mu
        self.t_mcmc[:, idx:idx + 1] = t
        self.tau_mcmc[:, idx:idx + 1] = tau

    def sample_T(self, mu, t, tau, Y):
        # Configure the limits based on the values in Y
        A = np.zeros(Y.shape)
        B = np.zeros(Y.shape)
        Q = Y.shape[0]
        N = Y.shape[1]
        eta = np.tile(mu, (Q, 1)) + np.tile(t, (1, N))
        Sigma = np.tile(tau, (1, N))
        A[W == 0] = -np.inf
        B[W == 1] = np.inf
        T = self.truncnorm(A, B, eta, Sigma)
        T[np.isnan(Y)] = np.nan
        return T

    def sample_mu(self, T, t, tau):
        tau_matrix = np.tile(tau.T, (self.Q, 1))
        tau_matrix[np.isnan(T)] = np.nan
        T_prime = T - np.tile(t, (1, self.N))
        T_prime = T_prime * tau_matrix
        S_tau = np.nansum(tau_matrix, axis=1, keepdims=True)
        mean = (np.nansum(T_prime, axis=1, keepdims=True) / (S_tau + self.tau_mu))
        var = 1.0 / (self.tau_mu + S_alpha)
        mu_out = np.sqrt(var) * np.random.randn(self.N, 1) + mean
        return mu_out

    def sample_t(self, T, mu, tau):
        tau_matrix = np.tile(tau.T, (self.Q, 1))
        tau_matrix[np.isnan(Z)] = np.nan
        T_prime = T - np.tile(mu, (self.Q, 1))
        T_prime = T_prime * tau_matrix
        S_alpha = np.nansum(tau_matrix, axis=0, keepdims=True)
        mean = (np.nansum(T_prime, axis=0, keepdims=True) / (S_alpha + self.tau_t))
        var = 1.0 / (self.tau_t + S_alpha)
        t_out = np.sqrt(var) * np.random.randn(1, self.Q) + mean
        return mu_out.T

    def sample_tau(self, T, mu, t):
        Zhat = Z - np.tile(mu.T, (self.Q, 1)) - np.tile(t, (1, self.N))
        D2 = Zhat ** 2 / 2
        N_obs = np.sum(~np.isnan(Zhat), axis=0)
        alpha_hat = self.alpha_alpha + N_obs / 2
        beta_hat = self.beta_alpha + np.nansum(D2, axis=0)
        out = np.random.gamma(alpha_hat, 1/beta_hat, self.Q)
        out.shape = (1, self.N)
        return out


    def fit(self, data, mu_init=None, t_init=None, tau_init=None):
        self.data = data # A numpy array of size Q (terms) x N (users)
        self.N, self.Q = data.shape
        self.K = int(np.max(data) + 1)

        # Initialize model parameters parameters according to priors
        if (mu_init is None):
            mu = np.sqrt(1/self.tau_mu) * np.random.randn(self.N, 1) + self.mu_theta
        else:
            mu = mu_init
        if (t_init is None):
            t = np.sqrt(1/self.tau_t) * np.random.randn(self.Q, 1) + self.mu_t
        else:
            t = t_init
        if (tau_init is None):
            tau = np.random.gamma(self.alpha_alpha, 1 / self.beta_alpha, size=(self.N, 1))
        else:
            tau = tau_init


        # Initialize the state variables
        self.setup_mcmc_samples()

        # Run the chain
        for tt in range(0, self.T):
            if ((tt + 1) % 1 == 0):
                print("Iter: " + str(t + 1))

            # Compute log liklihood
            # self.LL[t] = self.compute_LL(data, theta, alpha, beta, gamma)

            # Sample T
            T = self.sample_T(mu t, tau, data)

            # Sample mu
            mu = self.sample_mu(T, t, tau)

            # Sample t
            t = self.sample_t(T, mu, tau)

            # Sample tau
            tau = self.sample_tau(T, mu, t)

            # Save off values if t>burnin
            if (t >= self.burnin) & (((t - self.burnin) % self.thinning) == 0):
                self.save_samples(T, mu, tau, tt)

    def generate_synthetic_data(self, N, Q):
        # N participants responding to Q tasks, outcome is one of K discrete labels
        # Final matrices are N x Q

        # Generate the participant parameters
        mu = np.sqrt(1/self.tau_mu) * np.random.randn(N, 1) + self.mu_mu
        tau = np.random.gamma(self.alpha_tau, 1/self.beta_tau, size=(N, 1))

        # Generate the task parameters
        # Prior on C is dirichlet but we can just generate the label from a DU
        t = np.sqrt(1/self.tau_t) * np.random.randn(Q, 1) + self.mu_t

        # Generate T matrix of observed latent quantities
        T = np.tile(mu.T, (Q, 1)) + np.tile(t.T, (1, N))
        T = T + 1 / np.sqrt(np.tile(tau.T, (Q, 1))) * np.random.randn(Q, N)

        # Generate the actual observations
        Y = float(T > 0)

        return Y, T, mu, tau, t

