import rockit.*

%   *  
%   :\ L
%   : \   |
%    a \  |   H, M
%       \ |
%  Q _____. Centre of mass
%    | h
%    |
%    | l, m
%    | F


ocp = Ocp('T',12.0);

L = 2; % [m]
H = 1; % [m]
h = 0.5; % [m]
l = 0.5; % [m]
M = 60; % [kg]
m = 10; % [kg]
g = 9.81;

Rn = m*g*h;

alpha  = casadi.MX.sym('x');  % Rope angle wrt vertical (drawn pos)
beta   = casadi.MX.sym('x');  % Human angle wrt rope (drawn pos)
gamma  = casadi.MX.sym('x'); % Lower leg wrt to upper leg (draw +pi/2)
dalpha = casadi.MX.sym('x');  % Rope angle wrt vertical (drawn pos)
dbeta  = casadi.MX.sym('x'); % Human angle wrt rope (drawn pos)
dgamma = casadi.MX.sym('x');  % Lower leg wrt to upper leg (draw +pi/2)

R = casadi.MX.sym('u'); % Restore torque
T = casadi.MX.sym('u'); % Knee torque

delta = alpha-beta;
ddelta = dalpha-dbeta;

tau = delta-gamma+pi/2;
dtau = ddelta-dgamma;

q = [alpha; beta; gamma];
dq = [dalpha; dbeta; dgamma];

C = vertcat(L*sin(alpha), -L*cos(alpha));
Q = C+vertcat(-h*cos(delta), -h*sin(delta));
F = Q+vertcat(l*sin(tau),-l*cos(tau));
c = (Q+F)/2;

dC = jtimes(C,q,dq);
dQ = jtimes(Q,q,dq);
dc = jtimes(c,q,dq);

% Modeling with Lagrange mechanics
E_kin = 0.5*dtau^2*(m*l^2/12) + 0.5*ddelta^2*(M*H^2/12) + 0.5*M*sumsqr(dC) + 0.5*m*sumsqr(dc);
E_pot = M*g*C(2)+m*g*c(2);

Lag = E_kin - E_pot;

E_tot = E_kin + E_pot;

Lag_q = gradient(Lag,q);
Lag_dq = gradient(Lag,dq);

rhs = solve(jacobian(Lag_dq,dq),[0;R;T]+Lag_q-jtimes(Lag_dq,q,dq), 'symbolicqr');

%rhs = Lag_q;
matlab_serializer = StringSerializer();
matlab_serializer.pack(1);
matlab_deserializer = StringDeserializer(matlab_serializer.encode());
matlab_deserializer.unpack();
python_serializer = StringSerializer();
python_serializer.pack(1);
python_deserializer = StringDeserializer(python_serializer.encode());
python_deserializer.unpack();
python_serializer.connect(python_deserializer);
python_deserializer.connect(python_serializer);
matlab_serializer.connect(matlab_deserializer);
matlab_deserializer.connect(matlab_serializer);

matlab_serializer.pack(e);

ocp.set_der(dalpha, rhs(1));
