from brian2 import *
import matplotlib.pyplot as plt
prefs.codegen.target = "numpy"
import numpy as np

# Setting simulation parameters
n_neurons = 20
duration = 2*second
upper_current_limit = 10*uA/cm2

# LIF parameters

c = 1 * uF / cm2          # Membrane capacitance
g = 0.1 * mS / cm2        # Leak conductance
V_rest = -65 * mV         # Resting potential
V_th = -59 * mV           # Threshold-like parameter for quadratic term
D_t = 5 * mV              # Scaling for quadratic term
V_reset = -68 * mV        # Reset potential
tau_ref = 1.6 * ms        # Refractory period


# Defining equation for LIF model

eqs_LIF = '''
dV/dt = (1/c)*(-g*(V-V_rest)+I_stim) :volt (unless refractory)

I_stim :amp/meter**2

'''

# LIF simulation

population_LIF = NeuronGroup(N=n_neurons,
                             model=eqs_LIF,
                             threshold='V>=V_th',
                             reset='V=V_reset',
                             refractory=tau_ref,
                             method='exact')

population_LIF.V = V_rest
population_LIF.I_stim = 'upper_current_limit * i / (n_neurons-1)'

spikes_LIF = SpikeMonitor(population_LIF)
mon = StateMonitor(population_LIF, 'V', record=True)

# Creating network object
net_LIF = Network(population_LIF, spikes_LIF, mon)

# Run simulation for set duration
net_LIF.run(duration)

f_LIF = plt.figure("LIF f-i curve")
plot(population_LIF.I_stim/(uA/cm2), spikes_LIF.count / duration)
plt.xlabel('Input current density (µA/cm²)')
plt.ylabel('Firing Rate (spikes/s)')
plt.title('F-I curve (LIF)')
f_LIF.show()

# QIF parameters

c = 1 * uF / cm2          # Membrane capacitance
g = 0.1 * mS / cm2        # Leak conductance
V_rest = -65 * mV         # Resting potential
V_th = -50 * mV           # Threshold-like parameter for quadratic term
D_t = 5 * mV              # Scaling for quadratic term
V_reset = -68 * mV        # Reset potential
tau_ref = 1.7* ms         # Refractory period
I_th = 0.16* uA / cm2



# Defining equation for QIF model

eqs_QIF = '''
dV/dt = (1/c) * ((g / (2 * D_t)) * (V - V_th)**2 - I_th + I_stim) : volt (unless refractory)
I_stim : amp/meter**2

'''

# QIF simulation

population_QIF = NeuronGroup(n_neurons,
                             model=eqs_QIF,
                             threshold='V >= V_th',
                             reset='V = V_reset',
                             refractory=tau_ref,
                             method='euler')

population_QIF.V = V_rest      # Initial condition
population_QIF.I_stim = 'upper_current_limit * i / (n_neurons-1)'  # Set input current

# Set up monitors
spikes_QIF = SpikeMonitor(population_QIF)
mon_QIF = StateMonitor(population_QIF, 'V', record=True)

# Creating network object
net_QIF = Network(population_QIF, spikes_QIF, mon_QIF)

# Run simulation for set duration
net_QIF.run(duration)

f_QIF = plt.figure("QIF f-i curve")
plot(population_QIF.I_stim/(uA/cm2), spikes_QIF.count / duration)
plt.xlabel('Input current density [µA/cm²]')
plt.ylabel('Firing Rate [spikes/s]')
plt.title('F-I curve (QIF)')
f_QIF.show()

# EIF parameters

c = 1 * uF / cm2          # Membrane capacitance
g = 0.1 * mS / cm2        # Leak conductance
V_rest = -65 * mV         # Resting potential
V_th = -59 * mV           # Threshold parameter for exponential term
Delta_T = 2 * mV          # Sharpness parameter (specific to EIF)
V_reset = -70 * mV        # Reset potential
tau_ref = 1.3* ms         # Refractory period



# Defining equation for EIF model

eqs_EIF = '''
dV/dt = (1/c) * (-g * (V - V_rest) + g * Delta_T * exp((V - V_th) / Delta_T) + I_stim) : volt (unless refractory)
I_stim : amp/meter**2
'''

# EIF simulation

population_EIF = NeuronGroup(n_neurons,
                             model=eqs_EIF,
                             threshold='V >= V_th',
                             reset='V = V_reset',
                             refractory=tau_ref,
                             method='euler')

population_EIF.V = V_rest      # Initial condition
population_EIF.I_stim = 'upper_current_limit * i / (n_neurons-1)'  # Set input current

# Set up monitors
spikes_EIF = SpikeMonitor(population_EIF)
mon_EIF = StateMonitor(population_EIF, 'V', record=True)

# Creating network object

net_EIF = Network(population_EIF, spikes_EIF, mon_EIF)

# Run simulation for set duration

net_EIF.run(duration)

f_EIF = plt.figure("EIF f-i curve")
plot(population_EIF.I_stim/(uA/cm2), spikes_EIF.count / duration)
plt.xlabel('Input current density [µA/cm²]')
plt.ylabel('Firing Rate [spikes/s]')
plt.title('F-I curve (EIF)')
f_EIF.show()

# Comparison

f_comparison = plt.figure("LIF-QIF-EIF curve comparison")
plt.plot(population_LIF.I_stim/(uA/cm2), spikes_LIF.count / duration)
plt.plot(population_QIF.I_stim/(uA/cm2), spikes_QIF.count / duration)
plt.plot(population_EIF.I_stim/(uA/cm2), spikes_EIF.count / duration)
plt.legend(['LIF','QIF','EIF'])
plt.xlabel('Input current density [µA/cm²]')
plt.ylabel('Firing Rate [spikes/s]')
plt.title('F-I curve (comparison)')
f_comparison.show()


# Smoothed visualization

def smooth_moving_average_valid(data, window_size=3):
    """Smooth data using a moving average in 'valid' mode."""
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Set window size
window_size = 9

# Get the original data arrays
I_vals_LIF = population_LIF.I_stim/(uA/cm2)
fr_vals_LIF = spikes_LIF.count / duration

I_vals_QIF = population_QIF.I_stim/(uA/cm2)
fr_vals_QIF = spikes_QIF.count / duration

I_vals_EIF = population_EIF.I_stim/(uA/cm2)
fr_vals_EIF = spikes_EIF.count / duration

# Smooth the firing rate data using the moving average (valid mode)
smoothed_fr_LIF = smooth_moving_average_valid(fr_vals_LIF, window_size=window_size)
smoothed_fr_QIF = smooth_moving_average_valid(fr_vals_QIF, window_size=window_size)
smoothed_fr_EIF = smooth_moving_average_valid(fr_vals_EIF, window_size=window_size)


trim = window_size // 2
I_vals_LIF_trimmed = I_vals_LIF[trim:-trim]
I_vals_QIF_trimmed = I_vals_QIF[trim:-trim]
I_vals_EIF_trimmed = I_vals_EIF[trim:-trim]

# Plot the smoothed curves

f_smoothed = plt.figure("LIF-QIF-EIF smoothed curves")
plt.plot(I_vals_LIF_trimmed, smoothed_fr_LIF, label='LIF (smoothed)')
plt.plot(I_vals_QIF_trimmed, smoothed_fr_QIF, label='QIF (smoothed)')
plt.plot(I_vals_EIF_trimmed, smoothed_fr_EIF, label='EIF (smoothed)')
plt.legend(['LIF', 'QIF', 'EIF'])
plt.xlabel('Input current density [µA/cm²]')
plt.ylabel('Firing Rate [spikes/s]')
plt.title('F-I curve (smoothed)')
f_smoothed.show()

plt.show()
