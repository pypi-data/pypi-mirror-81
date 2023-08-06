from collections import Iterable

import cadquery as cq

from paramak import Shape


class RotateCircleShape(Shape):
    """Rotates a circular 3d CadQuery solid from a central point and a radius

    Args:
        points (a list of tuples each containing X (float), Z (float)): A list
            of a single XZ coordinate which is the central point of the circle.
            For example, [(10, 10)].
        radius (float): The radius of the circle.
        name (str): The legend name used when exporting a html graph of the
            shape.
        color (RGB or RGBA - sequences of 3 or 4 floats, respectively, each in the range 0-1):
            The color to use when exporting as html graphs or png images.
        material_tag (str): The material name to use when exporting the
            neutronics description.
        stp_filname (str): The filename used when saving stp files as part of a
            reactor.
        azimuth_placement_angle (float or iterable of floats): The angle or
            angles to use when rotating the shape on the azimuthal axis.
        rotation_angle (float): The rotation angle to use when revolving the
            solid (degrees).
        cut (CadQuery object): An optional CadQuery object to perform a boolean
            cut with this object.

    Returns:
        a paramak shape object: a Shape object that has generic functionality
    """

    def __init__(
        self,
        points,
        radius,
        workplane="XZ",
        stp_filename="RotateCircleShape.stp",
        stl_filename="RotateCircleShape.stl",
        solid=None,
        color=(0.5, 0.5, 0.5),
        azimuth_placement_angle=0,
        rotation_angle=360,
        cut=None,
        intersect=None,
        union=None,
        material_tag=None,
        name=None,
        **kwargs
    ):

        default_dict = {"tet_mesh": None,
                        "physical_groups": None,
                        "hash_value": None}

        for arg in kwargs:
            if arg in default_dict:
                default_dict[arg] = kwargs[arg]

        super().__init__(
            points=points,
            name=name,
            color=color,
            material_tag=material_tag,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            azimuth_placement_angle=azimuth_placement_angle,
            workplane=workplane,
            cut=cut,
            intersect=intersect,
            union=union,
            **default_dict
        )
        self.radius = radius
        self.rotation_angle = rotation_angle
        self.solid = solid

    @property
    def rotation_angle(self):
        return self._rotation_angle

    @rotation_angle.setter
    def rotation_angle(self, value):
        self._rotation_angle = value

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    def create_solid(self):
        """Creates a 3d solid using points, radius, azimuth_placement_angle and
           rotation_angle.

           Returns:
              A CadQuery solid: A 3D solid volume
        """

        solid = (
            cq.Workplane(self.workplane)
            .moveTo(self.points[0][0], self.points[0][1])
            .circle(self.radius)
            # .close()
            .revolve(self.rotation_angle)
        )

        if isinstance(self.azimuth_placement_angle, Iterable):
            rotated_solids = []
            # Perform seperate rotations for each angle
            for angle in self.azimuth_placement_angle:
                rotated_solids.append(
                    solid.rotate(
                        (0, 0, -1), (0, 0, 1), angle))
            solid = cq.Workplane(self.workplane)

            # Joins the seperate solids together
            for i in rotated_solids:
                solid = solid.union(i)
        else:
            # Peform rotations for a single azimuth_placement_angle angle
            solid = solid.rotate(
                (0, 0, -1), (0, 0, 1), self.azimuth_placement_angle)

        self.perform_boolean_operations(solid)

        return solid
