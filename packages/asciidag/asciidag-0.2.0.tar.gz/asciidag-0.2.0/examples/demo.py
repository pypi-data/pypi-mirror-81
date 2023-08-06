#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=bad-option-value,import-outside-toplevel
"""Demonstration of package functionality."""

from __future__ import absolute_import, division, print_function, unicode_literals


def main():
    """Run a simple demo of the package's functionality."""
    # start-after
    from asciidag.graph import Graph
    from asciidag.node import Node

    graph = Graph()

    root = Node('root')
    grandpa = Node('grandpa', parents=[root])
    tips = [
        Node('child', parents=[
            Node('mom', parents=[
                Node('grandma', parents=[
                    Node('greatgrandma', parents=[]),
                ]),
                grandpa,
            ]),
            Node('dad', parents=[
                Node('bill', parents=[
                    Node('martin'),
                    Node('james'),
                    Node('paul'),
                    Node('jon'),
                ])]),
            Node('stepdad', parents=[grandpa]),
        ]),
        Node('foo', [Node('bar')]),
    ]

    graph.show_nodes(tips)
    # end-before


if __name__ == '__main__':
    main()
