%
%     This file is part of rockit.
%
%     rockit -- Rapid Optimal Control Kit
%     Copyright (C) 2019 MECO, KU Leuven. All rights reserved.
%
%     Rockit is free software; you can redistribute it and/or
%     modify it under the terms of the GNU Lesser General Public
%     License as published by the Free Software Foundation; either
%     version 3 of the License, or (at your option) any later version.
%
%     Rockit is distributed in the hope that it will be useful,
%     but WITHOUT ANY WARRANTY; without even the implied warranty of
%     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
%     Lesser General Public License for mo/re details.
%
%     You should have received a copy of the GNU Lesser General Public
%     License along with CasADi; if not, write to the Free Software
%     Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
%
%


% Iterative learning example
% ==========================

import rockit.*

pendulum_ode = @(x,u,param) [x(2);(1/(param.I+param.m*param.L^2))*(-param.c*x(2) - 9.81*param.m*param.L*sin(x(1)) + u(1))];



def pendulum_simulator(x0, u, sim)
    xsim = getfield(horzcat(x0, sim.call(struct('x0', x0, 'p', u)),'xf'));
    return struct('xsim', xsim, 'ysim', squeeze(xsim[0, :-1]));
en

%Define problem parameter
plant_param = struct('m', 1,      'I', 1,     'L',1,      'c',1);
model_param = struct('m', 1.2,    'I', 1.2,   'L',0.9,    'c',0.9);
N = 100

T = 10;
tgrid = linspace(0, T, N);
y_ref_val = sin(tgrid);
x0 = [0, 0];

ocp = Ocp('t0',tgrid(1), 'T',tgrid[-1]);

% Define states
x = ocp.state(2);

% Define controls
u = ocp.control();

% Specify ODE
model_rhs = pendulum_ode(x, u, model_param);
ocp.set_der(x, model_rhs);

% Set initial conditions
ocp.subject_to(ocp.at_t0(x) == x0);

% Define reference
y_ref = ocp.parameter('grid','control');
ocp.set_value(y_ref, y_ref_val);

% Define output correction
beta = ocp.parameter('grid','control');

% Define previous control
u_prev = ocp.parameter('grid','control');


% Set ILC objective
ocp.add_objective(ocp.integral((y_ref - beta -x(1))^2,'grid','control')+1e-3*ocp.integral((u-u_prev)^2, 'grid','control'));

% Pick a solution method
ocp.solver('ipopt');

% Pick a solution method
ocp.method(MultipleShooting('N',N,'M',4,'intg','rk'));

% Define simulator for plant and model
plant_rhs = pendulum_ode(x, u, plant_param);

opts = struct('tf', T/N);

data = struct('x', x, 'p', u, 'ode', plant_rhs);
plant_sim = integrator('xkp1', 'cvodes', data, opts).mapaccum('simulator', N);

data = struct('x', x, 'p', u, 'ode', model_rhs);
model_sim = integrator('xkp1', 'cvodes', data, opts).mapaccum('simulator', N);

% Run ILC algorithm
u_prev_val = zeros(N);

y_meas = {};

num_its = 10;

for i = 1:num_its
    % Compute correction
    y_meas{end+1} = getfield(pendulum_simulator(x0, u_prev_val, plant_sim),'ysim');
    y_model = getfield(pendulum_simulator(x0, u_prev_val, model_sim),'ysim');
    beta_val = y_meas[-1] - y_model;
end

    % Set parameters for the current ILC iteration
    ocp.set_value(u_prev, u_prev_val);
    ocp.set_value(beta, beta_val);
end

    % Solve ILC problem
    sol = ocp.solve();
    t, 'u_prev_val',sol.sample(u', 'grid','control');
    t, 'x_val',sol.sample(x, 'grid','control');
    u_prev_val = u_prev_val[:-1];
end


    % plt.plot(tgrid, u_prev_val,'.-')
    % plt.plot(tgrid, y_ref_val,'.-')
    % plt.plot(tgrid, x_val[:-1,0],'-')
    % plt.legend(['u', 'pos ref ','position'])
    % plt.show(block=True)
end

% Plot last result
y_meas{end+1} = getfield(pendulum_simulator(x0, u_prev_val, plant_sim),'ysim');
y_first = asarray(y_meas(2));
y_last = asarray(y_meas[-1]);

figure();
plot(tgrid, y_ref_val,'.-');
plot(tgrid, y_first,'-');
plot(tgrid, y_last,'-');
legend(['reference', 'first measurement','last measurement']);
% plt.show(block=True)

err_norm_evol = zeros([num_its+1,1]);
for i = 1:num_its+1
    err_norm_evol(i) = norm_2(y_ref_val - y_meas(i));
end

figure();
plot(range(num_its+1), err_norm_evol,'-');
legend(['error norm']);
show('block',true);

% uval = np.zeros(N)
% y_plant = pendulum_simulator(x0, uval, plant_sim)['ysim']
% y_mod = pendulum_simulator(x0, uval, model_sim)['ysim']
%
% y_mod = np.asarray(y_mod)
% y_plant = np.asarray(y_plant)
%
% plt.plot(tgrid, y_mod,'-')
% plt.plot(tgrid, y_plant,'-')
% plt.show(block=True)
