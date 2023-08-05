# Solve a multi-commodity flow problem.

import gurobipy as gp
from gurobipy import GRB

# the minimum-cost network flow problem
def MCF(data):
    arcs = range(data["nArc"])
    nodes = range(data["nNode"])
    capacity = data["capacity"]
    cost = data["cost"]
    demand = data["demand"]
    origin = data["origin"]
    destination = data["destination"]

    m = gp.Model('netflow')
    flow = m.addVars(arcs, obj=cost, name="flow")

    # Arc-capacity constraints
    m.addConstrs(
        (flow.sum('*', e) <= capacity[e] for e in arcs), "cap")

    # Flow-conservation constraints
    m.addConstrs(
        (gp.quicksum(flow[e] for e in arcs if destination[e] == i)) >= demand[i] for i in nodes if demand[i] > 0)
    m.addConstrs((gp.quicksum(flow[e] for e in arcs if origin[e] == i)) <= -demand[i] for i in nodes if demand[i] < 0)
    m.addConstrs((gp.quicksum(flow[e] for e in arcs if origin[e] == i)) - (
        gp.quicksum(flow[e] for e in arcs if destination[e] == i)) == 0 for i in nodes if demand[i] == 0)

    m.optimize()

    # Print solution
    x = "None"
    status = "None"
    print (m.objVal)
    if m.status == GRB.OPTIMAL:
        status = "Optimal"
        solution = m.getAttr('X', flow)
        x = [solution[e] for e in arcs]
    else:
        status = "Infeasible"
    return {"status": status, "obj": m.objVal, "x": x}
