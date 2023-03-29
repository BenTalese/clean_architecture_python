from Application.Services.IPersistence import IPersistence
from Framework.Infrastructure.Persistence import Persistence

# TODO: Interfaces will have implementations in domain, application and framework...
INTERFACE_TO_CONCRETE = [
    (IPersistence, Persistence)
]
