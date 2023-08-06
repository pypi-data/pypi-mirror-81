from collections import Iterable

import cadquery as cq
import numpy as np
from scipy import integrate
from scipy.optimize import minimize

from paramak import ExtrudeMixedShape


class ToroidalFieldCoilPrincetonD(ExtrudeMixedShape):
    """Toroidal field coil based on Princeton-D curve

    Args:
        R1 (float): smallest radius (cm)
        R2 (float): largest radius (cm)
        thickness (float): magnet thickness (cm)
        distance (float): extrusion distance (cm)
        number_of_coils (int): the number of tf coils. This changes by the
            azimuth_placement_angle dividing up 360 degrees by the number of
            coils.
        vertical_displacement (float, optional): vertical displacement (cm).
            Defaults to 0.0.
        with_inner_leg (Boolean): Include the inner tf leg (default True)

    Keyword Args:
        stp_filename (str, optional): The filename used when saving stp files
            as part of a reactor.
            Defaults to "ToroidalFieldCoilPrincetonD.stp".
        stl_filename (str, optional): The filename used when saving stl files
            as part of a reactor.
            Defaults to "ToroidalFieldCoilPrincetonD.stl".
        color ((float, float, float), optional): the color to use when
            exportin as html graphs or png images. Defaults to None.
        azimuth_placement_angle (float, optional): The angle or angles to use
            when rotating the shape on the azimuthal axis. Defaults to 0.
        name (str, optional): the legend name used when exporting a html
            graph of the shape. Defaults to None.
        material_tag (str, optional): The material name to use when exporting
            the neutronics description.. Defaults to "outer_tf_coil_mat".
    """

    def __init__(
        self,
        R1,
        R2,
        thickness,
        distance,
        number_of_coils,
        vertical_displacement=0.0,
        stp_filename="ToroidalFieldCoilPrincetonD.stp",
        stl_filename="ToroidalFieldCoilPrincetonD.stl",
        color=(0.5, 0.5, 0.5),
        azimuth_placement_angle=0,
        name=None,
        material_tag="outer_tf_coil_mat",
        with_inner_leg=True,
        **kwargs
    ):

        default_dict = {
            "points": None,
            "workplane": "XZ",
            "solid": None,
            "intersect": None,
            "cut": None,
            "union": None,
            "tet_mesh": None,
            "physical_groups": None,
        }

        for arg in kwargs:
            if arg in default_dict:
                default_dict[arg] = kwargs[arg]

        super().__init__(
            distance=distance,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            color=color,
            azimuth_placement_angle=azimuth_placement_angle,
            material_tag=material_tag,
            name=name,
            hash_value=None,
            **default_dict
        )

        self.R1 = R1
        self.R2 = R2
        self.thickness = thickness
        self.distance = distance
        self.number_of_coils = number_of_coils
        self.vertical_displacement = vertical_displacement
        self.with_inner_leg = with_inner_leg

    @property
    def azimuth_placement_angle(self):
        self.find_azimuth_placement_angle()
        return self._azimuth_placement_angle

    @azimuth_placement_angle.setter
    def azimuth_placement_angle(self, value):
        self._azimuth_placement_angle = value

    def compute_inner_points(self, R1, R2):
        """Computes the inner curve points

        Args:
            R1 (float): smallest radius (cm)
            R2 (float): largest radius (cm)

        Returns:
            (list, list, list): R, Z and derivative lists for outer curve
                points
        """
        def error(Z0, R0, R2):
            segment = get_segment(R0, R2, Z0)
            return abs(segment[1][-1])

        def get_segment(a, b, Z0):
            a_R = np.linspace(a, b, num=70, endpoint=True)
            asol = integrate.odeint(solvr, [Z0, 0], a_R)
            return a_R, asol[:, 0], asol[:, 1]

        def solvr(Y, R):
            return [Y[1], -1 / (k * R) * (1 + Y[1]**2)**(3 / 2)]

        R0 = (R1 * R2)**0.5
        k = 0.5 * np.log(R2 / R1)

        # computing of Z0
        # Z0 is computed by ensuring outer segment end is zero
        Z0 = 10  # initial guess for Z0
        res = minimize(error, Z0, args=(R0, R2))
        Z0 = res.x

        # compute inner and outer segments
        segment1 = get_segment(R0, R1, Z0)
        segment2 = get_segment(R0, R2, Z0)

        R = np.concatenate([np.flip(segment1[0]), segment2[0]
                            [1:], np.flip(segment2[0])[1:], segment1[0][1:]])
        Z = np.concatenate([np.flip(segment1[1]), segment2[1]
                            [1:], -np.flip(segment2[1])[1:], -segment1[1][1:]])
        dz_dr = np.concatenate([np.flip(segment1[2]), segment2[2]])
        return R, Z, dz_dr

    def compute_outer_points(self, R, Z, thickness, derivative):
        """Computes outer curve points based on thickness

        Args:
            R (list): list of floats containing R values
            Z (list): list of floats containing Z values
            thickness (float): thickness of the magnet
            derivative (list): list of floats containing the first order
                derivatives

        Returns:
            (list, list): R and Z lists for outer curve points
        """
        R_outer, Z_outer = [], []
        for i in range(len(derivative)):
            nx = -derivative[i]
            ny = 1
            # normalise normal vector
            normal_vector_norm = (nx ** 2 + ny ** 2) ** 0.5
            nx /= normal_vector_norm
            ny /= normal_vector_norm
            # calculate outer points
            val_R_outer = R[i] + thickness * nx
            val_Z_outer = Z[i] + thickness * ny
            R_outer.append(val_R_outer)
            Z_outer.append(val_Z_outer)
        R_outer = np.concatenate([R_outer, np.flip(np.array(R_outer))])
        Z_outer = np.concatenate([Z_outer, np.flip(-np.array(Z_outer))])
        return R_outer, Z_outer

    def find_points(self):
        """Finds the XZ points joined by connections that describe the 2D
        profile of the toroidal field coil shape."""
        # compute inner and outer points
        R_inner, Z_inner, dz_dr = self.compute_inner_points(self.R1, self.R2)
        R_outer, Z_outer = self.compute_outer_points(
            R_inner, Z_inner, self.thickness, dz_dr)
        R_outer, Z_outer = np.flip(R_outer), np.flip(Z_outer)

        # add vertical displacement
        Z_outer += self.vertical_displacement
        Z_inner += self.vertical_displacement

        # extract helping points for inner leg
        inner_leg_connection_points = [
            (R_inner[0], Z_inner[0]),
            (R_inner[-1], Z_inner[-1]),
            (R_outer[0], Z_outer[0]),
            (R_outer[-1], Z_outer[-1])
        ]
        self.inner_leg_connection_points = inner_leg_connection_points

        # add the leg to the points
        if self.with_inner_leg:
            R_inner = np.append(R_inner, R_inner[0])
            Z_inner = np.append(Z_inner, Z_inner[0])

            R_outer = np.append(R_outer, R_outer[0])
            Z_outer = np.append(Z_outer, Z_outer[0])
        # add connections
        inner_points = [[r, z, 'spline'] for r, z in zip(R_inner, Z_inner)]
        outer_points = [[r, z, 'spline'] for r, z in zip(R_outer, Z_outer)]
        if self.with_inner_leg:
            outer_points[-2][2] = 'straight'
            inner_points[-2][2] = 'straight'

        inner_points[-1][2] = 'straight'
        outer_points[-1][2] = 'straight'

        points = inner_points + outer_points

        self.points = points

    def find_azimuth_placement_angle(self):
        """Calculates the azimuth placement angles based on the number of tf
        coils"""

        angles = list(
            np.linspace(
                0,
                360,
                self.number_of_coils,
                endpoint=False))

        self.azimuth_placement_angle = angles
