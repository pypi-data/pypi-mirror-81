# -*- coding: utf-8 -*-
"""
    This file contains the output management
"""
import logging
import copy

import numpy as np
import yaml

from . import interpolation
from .operator.member import OpMember
from .operator.physical import PhysicalOperator
from . import basis_rotation as br

logger = logging.getLogger(__name__)


class Output(dict):
    """
    Wrapper for the output to help with application
    to PDFs and dumping to file.
    """

    def apply_pdf(self, lhapdf_like, targetgrid=None, rotate_to_flavor_basis=True):
        """
        Apply all available operators to the input PDFs.

        Parameters
        ----------
            lhapdf_like : object
                object that provides an xfxQ2 callable (as lhapdf, ToyLH does) (and thus is
                in flavor basis)
            targetgrid : list
                if given, interpolates to the pdfs given at targetgrid (instead of xgrid)
            rotate_to_flavor_basis : boolean
                rotate output back to flavor basis

        Returns
        -------
            out_grid : dict
                output PDFs and their associated errors for the computed Q2grid
        """
        # turn lhapdf_like into list
        input_lists = br.generate_input_from_lhapdf(
            lhapdf_like, self["interpolation_xgrid"], self["q2_ref"]
        )

        # build output
        out_grid = {}
        for q2 in self["Q2grid"]:
            pdfs, errs = self.get_op(q2).apply_pdf(input_lists)
            out_grid[q2] = {"pdfs": pdfs, "errors": errs}

        # interpolate to target grid
        if targetgrid is not None:
            b = interpolation.InterpolatorDispatcher.from_dict(self, False)
            rot = b.get_interpolation(targetgrid)
            for q2 in out_grid:
                for pdf_label in out_grid[q2]["pdfs"]:
                    out_grid[q2]["pdfs"][pdf_label] = np.matmul(
                        rot, out_grid[q2]["pdfs"][pdf_label]
                    )
                    out_grid[q2]["errors"][pdf_label] = np.matmul(
                        rot, out_grid[q2]["errors"][pdf_label]
                    )
        # rotate?
        if rotate_to_flavor_basis:
            out_grid = self.rotate_pdfs_to_flavor_basis(out_grid)
        return out_grid

    @staticmethod
    def rotate_pdfs_to_flavor_basis(in_grid):
        """
        Rotate all PDFs from evolution basis to flavor basis

        Parameters
        ----------
            in_grid : dict
                a map q2 to pdfs and their errors in evolution basis

        Returns
        -------
            out_grid : dict
                updated map
        """
        out_grid = {}
        for q2, res in in_grid.items():
            out_grid[q2] = {k: br.rotate_output(v) for k, v in res.items()}
        return out_grid

    def get_raw(self):
        """
        Serialize result as dict/YAML.

        This maps the original numpy matrices to lists.

        Returns
        -------
            out : dict
                dictionary which will be written on output
        """
        # prepare output dict
        out = {
            "Q2grid": {},
        }
        # dump raw elements
        for f in ["interpolation_polynomial_degree", "interpolation_is_log", "q2_ref"]:
            out[f] = self[f]
        # make raw lists
        for k in ["interpolation_xgrid"]:
            out[k] = self[k].tolist()
        # make operators raw
        for q2 in self["Q2grid"]:
            out["Q2grid"][q2] = self.get_op(q2).to_raw()
        return out

    def dump_yaml(self, stream=None):
        """
        Serialize result as YAML.

        Parameters
        ----------
            stream : (Default: None)
                if given, dump is written on it

        Returns
        -------
            dump : any
                result of dump(output, stream), i.e. a string, if no stream is given or
                Null, if self is written sucessfully to stream
        """
        # TODO explicitly silence yaml
        out = self.get_raw()
        return yaml.dump(out, stream)

    def dump_yaml_to_file(self, filename):
        """
        Writes YAML representation to a file.

        Parameters
        ----------
            filename : string
                target file name

        Returns
        -------
            ret : any
                result of dump(output, stream), i.e. Null if written sucessfully
        """
        with open(filename, "w") as f:
            ret = self.dump_yaml(f)
        return ret

    @classmethod
    def load_yaml(cls, stream):
        """
        Load YAML representation from stream

        Parameters
        ----------
            stream : any
                source stream

        Returns
        -------
            obj : output
                loaded object
        """
        obj = yaml.safe_load(stream)
        return cls(obj)

    @classmethod
    def load_yaml_from_file(cls, filename):
        """
        Load YAML representation from file

        Parameters
        ----------
            filename : string
                source file name

        Returns
        -------
            obj : output
                loaded object
        """
        obj = None
        with open(filename) as o:
            obj = Output.load_yaml(o)
        return obj

    def get_op(self, q2):
        """
        Load a :class:`PhysicalOperator` from the raw data.

        Parameters
        ----------
            q2 : float
                target scale

        Returns
        -------
            op : PhysicalOperator
                corresponding Operator
        """
        # check existence
        if q2 not in self["Q2grid"]:
            raise KeyError(f"q2={q2} not in grid")
        # compose
        ops = self["Q2grid"][q2]
        op_members = {}
        for name in ops["operators"]:
            op_members[name] = OpMember(
                ops["operators"][name], ops["operator_errors"][name], name
            )
        return PhysicalOperator(op_members, q2)

    def concat(self, other):
        """
        Concatenate (multiply) two outputs.

        Parameters
        ----------
            other : Output
                other factor to be multiplied from the left, i.e. with *smaller* intial scale

        Returns
        -------
            out : Output
                self * other
        """
        # check type
        if not isinstance(other, Output):
            raise ValueError("can only concatenate two Output instances!")
        # check parameters
        for f in ["interpolation_polynomial_degree", "interpolation_is_log"]:
            if not self[f] == other[f]:
                raise ValueError(
                    f"'{f}' of the two factors does not match: {self[f]} vs {other[f]}"
                )
        if not np.allclose(self["interpolation_xgrid"], other["interpolation_xgrid"]):
            raise ValueError("'interpolation_xgrid' of the two factors does not match")
        # check matching
        mid_scale = self["q2_ref"]
        if not mid_scale in other["Q2grid"]:
            raise ValueError("Operators can not be joined")
        # prepare output
        other_op = other.get_op(mid_scale)
        out = copy.deepcopy(self)
        out["q2_ref"] = other["q2_ref"]
        for q2 in self["Q2grid"]:
            # multiply operators
            me = self.get_op(q2)
            prod = me * other_op
            out["Q2grid"][q2] = prod.to_raw()

        return out
