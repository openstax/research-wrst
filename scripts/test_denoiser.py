from denoiser import WRSTDenoiser
import numpy as np
from scipy.stats import mode

# User params
N = 100
Q = 100
K = 5

# Generate synthetic data
denoiser = WRSTDenoiser()
denoiser.K = K
denoiser.N = N
denoiser.Q = Q
L, Z, W, F, C, theta, mu, alpha = denoiser.generate_synthetic_data(N, Q, 5)

# Run .fit()
# denoiser.N = N
# denoiser.Q = Q
#denoiser.fit(L, C_init=C) #, theta_init=theta, mu_init=mu, W_init=W, C_init=C, F_init=F)
#
#theta_hat = np.mean(denoiser.theta_mcmc, axis=1, keepdims=True)
#mu_hat = np.mean(denoiser.mu_mcmc, axis=1, keepdims=True)


# # Do some analyses?
# theta_mcmc = np.zeros((N, 100))
# for ii in range(100):
#     theta_mcmc[:, ii:ii+1] = denoiser.sample_theta(Z, mu, alpha)
# theta_hat = np.mean(theta_mcmc, axis=1, keepdims=True)
# e_theta = np.mean(np.abs((theta_hat - theta)))
#
# mu_mcmc = np.zeros((Q, 100))
# for ii in range(100):
#     mu_mcmc[:, ii:ii+1] = denoiser.sample_mu(Z, theta, alpha)
# mu_hat = np.mean(mu_mcmc, axis=1, keepdims=True)
# e_mu = np.mean(np.abs((mu_hat - mu)))
#
# alpha_mcmc = np.zeros((Q, 100))
# for ii in range(100):
#     alpha_mcmc[:, ii:ii+1] = denoiser.sample_alpha(Z, theta, alpha)
# alpha_hat = np.mean(alpha_mcmc, axis=1, keepdims=True)
# e_alpha = np.mean(np.abs((alpha_hat - alpha)))

C_mcmc = np.zeros((Q, 100))
F_mcmc = np.zeros((Q, K))
for ii in range(100):
    Ct, Ft = denoiser.sample_CF(Z, L)
    Ct.shape = (len(Ct), 1)
    C_mcmc[:, ii:ii+1] = Ct
    F_mcmc += F_t
C_hat = mode(C_mcmc, axis=1)[0]
C.shape = (Q, 1)
e_c = np.mean(C_hat != C)
e_f = np.mean(np.abs(F_mcmc-Ft))