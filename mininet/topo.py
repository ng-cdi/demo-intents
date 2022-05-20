#!/usr/bin/env python

from __future__ import annotations

from pathlib import Path
import re
import json
import signal
from typing import TYPE_CHECKING, TypedDict, Optional
from dataclasses import dataclass
from threading import Event
from mtv.link import TCLink
from mtv.net import Mininet
from mtv.rest import REST
from mtv.cli import CLI
from mtv.node import (
    RemoteController,
    OVSSwitch,
    DefaultController,
    OVSKernelSwitch,
    Switch,
    DynamipsRouter,
)
from mtv.node import Node as MTVNode



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
    interfaces: dict[int, tuple[str, str, list[tuple[int, str]]]]
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
    interfaces: dict[str, tuple[str, str]]
    instance: Optional[MTVNode]


net = Mininet(switch=OVSSwitch, build=False, topo=None, link=TCLink)


def do_inferred_topo():
    switches = {
        "s5": {"params": {"name": "s5", "dpid": "0000000000000005"}},
        "s7": {"params": {"name": "s7", "dpid": "0000000000000007"}},
        "s2": {"params": {"name": "s2", "dpid": "0000000000000002"}},
        "s3": {"params": {"name": "s3", "dpid": "0000000000000003"}},
        "s1": {"params": {"name": "s1", "dpid": "0000000000000001"}},
        "s8": {"params": {"name": "s8", "dpid": "0000000000000008"}},
        "s11": {"params": {"name": "s11", "dpid": "000000000000000b"}},
        "s14": {"params": {"name": "s14", "dpid": "000000000000000e"}},
        "s12": {"params": {"name": "s12", "dpid": "000000000000000c"}},
        "s9": {"params": {"name": "s9", "dpid": "0000000000000009"}},
        "s10": {"params": {"name": "s10", "dpid": "000000000000000a"}},
        "s4": {"params": {"name": "s4", "dpid": "0000000000000004"}},
        "s6": {"params": {"name": "s6", "dpid": "0000000000000006"}},
        "s13": {"params": {"name": "s13", "dpid": "000000000000000d"}},
    }
    hosts = {
        "h7": {"params": {"name": "h7", "ip": "10.0.0.7", "mac": "00:00:00:00:00:07"}},
        "h9": {"params": {"name": "h9", "ip": "10.0.0.9", "mac": "00:00:00:00:00:09"}},
        "h6": {"params": {"name": "h6", "ip": "10.0.0.6", "mac": "00:00:00:00:00:06"}},
        "h5": {"params": {"name": "h5", "ip": "10.0.0.5", "mac": "00:00:00:00:00:05"}},
        "h3": {"params": {"name": "h3", "ip": "10.0.0.3", "mac": "00:00:00:00:00:03"}},
        "h4": {"params": {"name": "h4", "ip": "10.0.0.4", "mac": "00:00:00:00:00:04"}},
        "h1": {"params": {"name": "h1", "ip": "10.0.0.1", "mac": "00:00:00:00:00:01"}},
        "h2": {"params": {"name": "h2", "ip": "10.0.0.2", "mac": "00:00:00:00:00:02"}},
        "h8": {"params": {"name": "h8", "ip": "10.0.0.8", "mac": "00:00:00:00:00:08"}},
    }
    switch_links = [
        [{"name": "s10", "port": 6}, {"name": "s13", "port": 3}],
        [{"name": "s10", "port": 3}, {"name": "s5", "port": 3}],
        [{"name": "s2", "port": 3}, {"name": "s8", "port": 2}],
        [{"name": "s1", "port": 2}, {"name": "s7", "port": 1}],
        [{"name": "s12", "port": 8, "bw": 1000}, {"name": "s14", "port": 3}],
        [{"name": "s6", "port": 3}, {"name": "s10", "port": 4}],
        [{"name": "s7", "port": 3}, {"name": "s12", "port": 2}],
        [{"name": "s6", "port": 2}, {"name": "s11", "port": 2}],
        [{"name": "s12", "port": 3}, {"name": "s8", "port": 3}],
        [{"name": "s7", "port": 2}, {"name": "s2", "port": 2}],
        [{"name": "s14", "port": 4, "bw": 1000}, {"name": "s13", "port": 6}],
        [{"name": "s13", "port": 4}, {"name": "s11", "port": 4}],
        [{"name": "s10", "port": 5}, {"name": "s12", "port": 5}],
        [{"name": "s11", "port": 5}, {"name": "s14", "port": 2}],
        [{"name": "s9", "port": 5}, {"name": "s13", "port": 2}],
        [{"name": "s10", "port": 2}, {"name": "s4", "port": 3}],
        [{"name": "s9", "port": 3}, {"name": "s4", "port": 2}],
        [{"name": "s12", "port": 7, "bw": 1000}, {"name": "s13", "port": 5}],
        [{"name": "s3", "port": 2}, {"name": "s9", "port": 2}],
        [{"name": "s3", "port": 3}, {"name": "s10", "port": 1}],
        [{"name": "s9", "port": 4}, {"name": "s12", "port": 4}],
        [{"name": "s11", "port": 1}, {"name": "s5", "port": 2}],
        [{"name": "s8", "port": 1}, {"name": "s1", "port": 3}],
        [{"name": "s11", "port": 3}, {"name": "s12", "port": 6}],
        [{"name": "s9", "port": 1}, {"name": "s2", "port": 4}],
    ]
    host_links = [
        [
            {"name": "h7", "mac": "00:00:00:00:00:07", "intf": "h7-eth0", "bw": 1000},
            {"name": "s12", "port": 1},
        ],
        [
            {"name": "h9", "mac": "00:00:00:00:00:09", "intf": "h9-eth0", "bw": 1000},
            {"name": "s14", "port": 1},
        ],
        [
            {"name": "h6", "mac": "00:00:00:00:00:06", "intf": "h6-eth0"},
            {"name": "s6", "port": 1},
        ],
        [
            {"name": "h5", "mac": "00:00:00:00:00:05", "intf": "h5-eth0"},
            {"name": "s5", "port": 1},
        ],
        [
            {"name": "h3", "mac": "00:00:00:00:00:03", "intf": "h3-eth0"},
            {"name": "s3", "port": 1},
        ],
        [
            {"name": "h4", "mac": "00:00:00:00:00:04", "intf": "h4-eth0"},
            {"name": "s4", "port": 1},
        ],
        [
            {"name": "h1", "mac": "00:00:00:00:00:01", "intf": "h1-eth0"},
            {"name": "s1", "port": 1},
        ],
        [
            {"name": "h2", "mac": "00:00:00:00:00:02", "intf": "h2-eth0"},
            {"name": "s2", "port": 1},
        ],
        [
            {"name": "h8", "mac": "00:00:00:00:00:08", "intf": "h8-eth0", "bw": 1000},
            {"name": "s13", "port": 1},
        ],
    ]

    net.addController("c0", controller=RemoteController, ip="127.0.0.1", port=6633)

    for switch in switches.values():
        switch["instance"] = net.addSwitch(cls=OVSKernelSwitch, batch=True, failMode="standalone", protocols="OpenFlow13", **switch["params"])

    for host in hosts.values():
        host["instance"] = net.addHost(**host["params"])

    for src, dst in switch_links:
        net.addLink(
            switches[src["name"]]["instance"],
            switches[dst["name"]]["instance"],
            port1=src["port"],
            port2=dst["port"],
            bw=src.get("bw", 100),
        )

    for src, dst in host_links:
        net.addLink(
            hosts[src["name"]]["instance"],
            switches[dst["name"]]["instance"],
            port2=dst["port"],
            bw=src.get("bw", 100),
        )

    def post_build():
        for src, _ in host_links:
            host = hosts[src["name"]]["instance"]
            host.intf(src["intf"]).setMAC(src["mac"])

        for name, host in hosts.items():
            if name in ["h7", "h8", "h9"]:
                continue

            inst = host["instance"]
            inst.cmd(f"ip route add 2.128.0.0/24 via 10.0.0.2")
            inst.cmd(f"ip route add 2.128.1.0/24 via 10.0.0.2")

        hosts["h7"]["instance"].cmd(f"iptables -t nat -I POSTROUTING -o h7-eth1 -j SNAT --to 2.128.0.101")

    return post_build


############################
#
#  batfish stuff
#
############################

dynamips_image = str(Path(__file__).parent / "c7200-adventerprisek9-mz.153-3.XB12.image")

def do_batfish():
    root_dir = Path(__file__).parent.parent / "batfish"
    with open(root_dir / "example_layer1_topology.json") as f:
        topo: Topology = json.load(f)

    routers: dict[str, Router] = {}
    hosts: dict[str, Host] = {}
    links: list[tuple[str, str, Optional[int], Optional[int]]] = []

    pd_map = {"GigabitEthernet": "PA-GE"}

    def parse_host_interface(intf: str) -> Optional[int]:
        m = re.match(r"eth(?P<port>\d+)", intf)

        if m is None:
            return None

        return int(m.group("port"))

    def parse_router_interface(intf: str) -> tuple[str, str, int, int]:
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
            dynamips_image=dynamips_image,
            dynamips_args=[
                "-i {}".format(i),
                "--idle-pc=0x60630338",
                "-P 7200",
                "-o 64",
                "-r 200",
            ],
        )

    for host in hosts.values():
        host.instance = net.get(host.hostname)  # type: ignore

    for l, r, lp, rp in links:
        if l == r:
            print("skipping {}-{}, loop".format(l, r))
            continue
        net.addLink(l, r, lp, rp)

    def post_start():
        net.waitConnected()

        for host in hosts.values():
            for name, (prefix, gateway) in host.interfaces.items():
                assert host.instance is not None
                iname = f"{host.hostname}-{name}"
                host.instance.setIP(prefix, intf=iname)
                host.instance.setDefaultRoute(f"dev {iname} via {gateway}")
                # host.instance.cmd("ip route add 10.0.0.0/24 via eth0")

    return post_start

def add_inter():
    h50 = net.addSwitch(
        "h50",
        cls=DynamipsRouter,
        dynamips_platform="7200",
        dynamips_image=dynamips_image,
        dynamips_args=[
            "-i {}".format("h10"),
            "--idle-pc=0x60630338",
            "-P 7200",
            "-o 64",
            "-r 200",
        ],
        dynamips_console_port=7123,
        dynamips_port_driver=("PA-FE-TX", "FastEthernet", 1),
    )
    net.addLink("s6", h50, params2={"ip": "10.0.0.50/24"}, addr2="00:00:00:00:00:32")

    def post_build():
        pass
        # h50.intf("h50-eth0").setMAC("00:00:00:00:00:32")

    return post_build

# h1 ip r add 2.128.0.0/24 via 10.0.0.2
# h1 ip r add 2.128.1.0/24 via 10.0.0.2

post_build = do_inferred_topo()
post_start = do_batfish()
post_build_2 = add_inter()

print("Added everything, starting up")

net.build()
post_build()
post_build_2()
net.start()
net.staticArp()
post_start()
net.pingAll()

print("Finished startup")

REST(net)
CLI(net)

net.stop()
