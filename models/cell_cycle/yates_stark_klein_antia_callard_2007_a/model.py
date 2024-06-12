# Size of variable arrays:
sizeAlgebraic = 0
sizeStates = 2
sizeConstants = 5
from math import *
from numpy import *

def createLegends():
    legend_states = [""] * sizeStates
    legend_rates = [""] * sizeStates
    legend_algebraic = [""] * sizeAlgebraic
    legend_voi = ""
    legend_constants = [""] * sizeConstants
    legend_voi = "time in component environment (day)"
    legend_states[0] = "x in component x (dimensionless)"
    legend_constants[0] = "d1 in component model_parameters (first_order_rate_constant)"
    legend_constants[1] = "a in component model_parameters (first_order_rate_constant)"
    legend_constants[2] = "r in component model_parameters (first_order_rate_constant)"
    legend_states[1] = "y in component y (dimensionless)"
    legend_constants[3] = "kappa in component model_parameters (dimensionless)"
    legend_constants[4] = "d2 in component model_parameters (first_order_rate_constant)"
    legend_rates[0] = "d/dt x in component x (dimensionless)"
    legend_rates[1] = "d/dt y in component y (dimensionless)"
    return (legend_states, legend_algebraic, legend_voi, legend_constants)

def initConsts():
    constants = [0.0] * sizeConstants; states = [0.0] * sizeStates;
    states[0] = 10E-1
    constants[0] = 0.005
    constants[1] = 0.03333
    constants[2] = 1.0
    states[1] = 0.0
    constants[3] = 1.0
    constants[4] = (-(99.0000*constants[1]*constants[0])+constants[1]*constants[2]+constants[0]*constants[2])/(constants[1]-constants[0])
    return (states, constants)

def computeRates(voi, states, constants):
    rates = [0.0] * sizeStates; algebraic = [0.0] * sizeAlgebraic
    rates[0] = 2.00000*constants[2]*states[1]-(constants[1]*states[0]*(1.00000-states[0]/constants[3])+constants[0]*states[0]*(states[0]/constants[3]))
    rates[1] = constants[1]*states[0]*(1.00000-states[0]/constants[3])-(constants[2]+constants[4])*states[1]
    return(rates)

def computeAlgebraic(constants, states, voi):
    algebraic = array([[0.0] * len(voi)] * sizeAlgebraic)
    states = array(states)
    voi = array(voi)
    return algebraic

def solve_model():
    """Solve model with ODE solver"""
    from scipy.integrate import ode
    # Initialise constants and state variables
    (init_states, constants) = initConsts()

    # Set timespan to solve over
    voi = linspace(0, 10, 500)

    # Construct ODE object to solve
    r = ode(computeRates)
    r.set_integrator('vode', method='bdf', atol=1e-06, rtol=1e-06, max_step=1)
    r.set_initial_value(init_states, voi[0])
    r.set_f_params(constants)

    # Solve model
    states = array([[0.0] * len(voi)] * sizeStates)
    states[:,0] = init_states
    for (i,t) in enumerate(voi[1:]):
        if r.successful():
            r.integrate(t)
            states[:,i+1] = r.y
        else:
            break

    # Compute algebraic variables
    algebraic = computeAlgebraic(constants, states, voi)
    return (voi, states, algebraic)

def plot_model(voi, states, algebraic):
    """Plot variables against variable of integration"""
    import pylab
    (legend_states, legend_algebraic, legend_voi, legend_constants) = createLegends()
    pylab.figure(1)
    pylab.plot(voi,vstack((states,algebraic)).T)
    pylab.xlabel(legend_voi)
    pylab.legend(legend_states + legend_algebraic, loc='best')
    pylab.show()

if __name__ == "__main__":
    (voi, states, algebraic) = solve_model()
    plot_model(voi, states, algebraic)