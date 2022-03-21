#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, TypedDict

from mtv.cli import CLI
from mtv.net import Mininet
from mtv.node import DynamipsRouter
from mtv.node import Node as MTVNode
from mtv.node import Switch

root_dir = Path(__file__).parent


class Topology(TypedDict):
    edges: list[Link]


class Link(TypedDict):
    node1: Node
    node2: Node


class Node(TypedDict):
    hostname: str
    interfaceName: str


@dataclass
class Router:
    hostname: str
    cfg: str
    interfaces: dict[int, Tuple[str, str, list[Tuple[int, str]]]]
    instance: Optional[Switch]

    def add_interface(
        self, pd: str, type_: str, slot: int, index: int, other_side: str
    ):
        if slot in self.interfaces:
            e_pd, e_type_, ports = self.interfaces[slot]
            assert (e_pd == pd) and (e_type_ == type_)

            ports.append((index, other_side))
        else:
            self.interfaces[slot] = (pd, type_, [(index, other_side)])


@dataclass
class Host:
    hostname: str
    interfaces: dict[str, Tuple[str, str]]
    instance: Optional[MTVNode]


# exploring the topology is probably the best way to discover
# routers and their interfaces

with open(root_dir / "example_layer1_topology.json") as f:
    topo: Topology = json.load(f)


routers: dict[str, Router] = {}
hosts: dict[str, Host] = {}
links: list[Tuple[str, str, Optional[int], Optional[int]]] = []

pd_map = {"GigabitEthernet": "PA-GE"}


def parse_host_interface(intf: str) -> Optional[int]:
    m = re.match(r"eth(?P<port>\d+)", intf)

    if m is None:
        return None

    return int(m.group("port"))


def parse_router_interface(intf: str) -> Tuple[str, str, int, int]:
    m = re.match(r"(?P<port_driver>\w+)(?P<slot>\d+)/(?P<index>\d+)", intf)

    assert m is not None

    type_ = m.group("port_driver")
    slot = int(m.group("slot"))
    index = int(m.group("index"))

    pd = pd_map[type_]

    return pd, type_, slot, index


def insert_router(node: Node, cfg_path: Path, other_side: str):
    if node["hostname"] not in routers:
        with open(cfg_path) as f:
            cfg = f.read()

        routers[node["hostname"]] = Router(node["hostname"], cfg, {}, None)

    pd, type_, slot, index = parse_router_interface(node["interfaceName"])
    routers[node["hostname"]].add_interface(pd, type_, slot, index, other_side)


def insert_host(node: Node):
    if node["hostname"] not in hosts:
        cfg_path = root_dir / "live" / "hosts" / f'{node["hostname"]}.json'

        with open(cfg_path) as f:
            cfg = json.load(f)

        interfaces = {
            o["name"]: (o["prefix"], o["gateway"])
            for o in cfg["hostInterfaces"].values()
        }

        hosts[node["hostname"]] = Host(node["hostname"], interfaces, None)


def insert_node(node: Node, other_side: Node):
    router_cfg_path = root_dir / "live" / "configs" / f'{node["hostname"]}.cfg'

    if router_cfg_path.exists():
        insert_router(node, router_cfg_path, other_side["hostname"])
    else:
        insert_host(node)


seen_links = set()

for link in topo["edges"]:
    node1 = link["node1"]
    node2 = link["node2"]

    if (node1["hostname"], node2["hostname"]) in seen_links:
        continue
    if (node2["hostname"], node1["hostname"]) in seen_links:
        continue

    seen_links.add((node1["hostname"], node2["hostname"]))

    links.append(
        (
            node1["hostname"],
            node2["hostname"],
            parse_host_interface(node1["interfaceName"]),
            parse_host_interface(node2["interfaceName"]),
        )
    )
    insert_node(node1, node2)
    insert_node(node2, node1)

# print(routers)
# print(hosts)
# print(links)

net = Mininet()

c1 = net.addController("c1")

for i, router in enumerate(routers.values()):
    ports = [
        (pd, type_, slot, links)
        for slot, (pd, type_, links) in router.interfaces.items()
    ]

    router.instance = net.addSwitch(
        router.hostname,
        cls=DynamipsRouter,
        dynamips_config=router.cfg,
        dynamips_ports=ports,
        dynamips_platform="7200",
        dynamips_image="/home/ben/Downloads/c7200-adventerprisek9-mz.153-3.XB12.image",
        dynamips_args=[
            "-i {}".format(i),
            "--idle-pc=0x619d25bc",
            "-P 7200",
            "-o 64",
            "-r 200",
        ],
    )

for host in hosts.values():
    host.instance = net.addHost(
        host.hostname,
        # TODO: iptables
    )

for l, r, lp, rp in links:
    if l == r:
        print("skipping {}-{}, loop".format(l, r))
        continue
    net.addLink(l, r, lp, rp)

print("Initialising")
net.start()
print("Waiting for routers to boot")
net.waitConnected()

for host in hosts.values():
    for name, (prefix, gateway) in host.interfaces.items():
        assert host.instance is not None
        iname = "{}-{}".format(host.hostname, name)
        host.instance.setIP(prefix) #, intf=iname)
        host.instance.setDefaultRoute("dev {} via {}".format(iname, gateway))

CLI(net)

net.stop()
