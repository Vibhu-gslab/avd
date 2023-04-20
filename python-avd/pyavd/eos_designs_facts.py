from collections import ChainMap

from .vendor.eos_designs.eos_designs_facts import EosDesignsFacts


def eos_designs_facts(all_hostvars: dict[str, dict]) -> dict[str, dict]:
    """
    Render eos_designs_facts from hostvars.

    Note! No support for inline templating or jinja templates for descriptions or ip addressing

    Parameters
    ----------
    all_hostvars : dict
        hostname1 : dict
        hostname2 : dict

    Returns
    -------
    dict
        avd_switch_facts : dict
        avd_overlay_peers : dict
        avd_topology_peers : dict
    """

    avd_switch_facts_instances = create_avd_switch_facts_instances(all_hostvars)

    avd_switch_facts = render_avd_switch_facts(avd_switch_facts_instances)
    avd_overlay_peers, avd_topology_peers = render_peers(avd_switch_facts)

    return {
        "avd_switch_facts": avd_switch_facts,
        "avd_overlay_peers": avd_overlay_peers,
        "avd_topology_peers": avd_topology_peers,
    }


def create_avd_switch_facts_instances(all_hostvars: dict):
    """
    Create "avd_switch_facts_instances" dictionary

    Parameters
    ----------
    all_hostvars : dict
        hostname1 : dict
        hostname2 : dict

    Returns
    -------
    dict
        hostname1 : dict
            switch : <EosDesignsFacts object>,
        hostname2 : dict
            switch : <EosDesignsFacts object>,
        ...
    """
    avd_switch_facts = {}
    for hostname, vars in all_hostvars.items():
        hostvars = ChainMap(
            # All the AVD code looks for the hostname in this key.
            {"inventory_hostname": hostname},
            vars,
        )

        # Add reference to dict "avd_switch_facts".
        # This is used to access EosDesignsFacts objects of other switches during rendering of one switch.
        hostvars["avd_switch_facts"] = avd_switch_facts

        # Notice templar is set as None, so any calls to jinja templates will fail with Nonetype has no "_loader" attribute
        avd_switch_facts[hostname] = {"switch": EosDesignsFacts(hostvars=hostvars, templar=None)}

        # Add reference to EosDesignsFacts object inside hostvars.
        # This is used to allow templates to access the facts object directly with "switch.*"
        hostvars["switch"] = avd_switch_facts[hostname]["switch"]

    return avd_switch_facts


def render_avd_switch_facts(avd_switch_facts_instances: dict):
    """
    Run the render method on each EosDesignsFacts object

    Parameters
    ----------
    avd_switch_facts_instances : dict of EosDesignsFacts

    Returns
    -------
    dict
        hostname1 : dict
            switch : < switch.* facts >
        hostname2 : dict
            switch : < switch.* facts >
    """
    return {hostname: {"switch": avd_switch_facts_instances[hostname]["switch"].render()} for hostname in avd_switch_facts_instances}


def render_peers(avd_switch_facts: dict) -> tuple[dict, dict]:
    """
    Build dicts of underlay and overlay peerings based on avd_switch_facts

    Parameters
    ----------
    avd_switch_facts : dict
        hostname1 : dict
            switch : < switch.* facts >
        hostname2 : dict
            switch : < switch.* facts >

    Returns
    -------
    avd_overlay_peers: dict
        hostname1 : list[str]
            List of switches pointing to hostname1 as route server / route reflector
        hostname2 : list[str]
            List of switches pointing to hostname2 as route server / route reflector
    avd_topology_peers: dict
        hostname1 : list[str]
            List of switches having hostname1 as uplink_switch
        hostname2 : list[str]
            List of switches having hostname2 as uplink_switch

    """

    avd_overlay_peers = {}
    avd_topology_peers = {}
    for hostname in avd_switch_facts:
        host_evpn_route_servers = avd_switch_facts[hostname]["switch"].get("evpn_route_servers", [])
        for peer in host_evpn_route_servers:
            avd_overlay_peers.setdefault(peer, []).append(hostname)

        host_mpls_route_reflectors = avd_switch_facts[hostname]["switch"].get("mpls_route_reflectors", [])
        for peer in host_mpls_route_reflectors:
            avd_overlay_peers.setdefault(peer, []).append(hostname)

        host_topology_peers = avd_switch_facts[hostname]["switch"].get("uplink_peers", [])

        for peer in host_topology_peers:
            avd_topology_peers.setdefault(peer, []).append(hostname)

    return avd_overlay_peers, avd_topology_peers
