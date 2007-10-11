#    Copyright 2007 John Kasunich and Jeff Epler
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import rs274.OpenGLTk, Tkinter
from minigl import *

class Collection:
    def __init__(self, parts):
	self.parts = parts

    def traverse(self):
	for p in self.parts:
	    if hasattr(p, "apply"):
		p.apply()
	    if hasattr(p, "capture"):
		p.capture()
	    if hasattr(p, "draw"):
		p.draw()
	    if hasattr(p, "traverse"):
		p.traverse()
	    if hasattr(p, "unapply"):
		p.unapply()

class Translate(Collection):
    def __init__(self, parts, x, y, z):
	self.parts = parts
	self.where = x, y, z

    def apply(self):
	glPushMatrix()
	glTranslatef(*self.where)

    def unapply(self):
	glPopMatrix()

class HalTranslate(Collection):
    def __init__(self, parts, comp, var, x, y, z):
	self.parts = parts
	self.where = x, y, z
	self.comp = comp
	self.var = var

    def apply(self):
	x, y, z = self.where
	v = self.comp[self.var]
	
	glPushMatrix()
	glTranslatef(x*v, y*v, z*v)

    def unapply(self):
	glPopMatrix()

class Scale(Collection):
    def __init__(self, parts, x, y, z):
	self.parts = parts
	self.where = x, y, z

    def apply(self):
	glPushMatrix()
	glScalef(*self.where)

    def unapply(self):
	glPopMatrix()

class HalScale(Collection):
    def __init__(self, parts, comp, var, x, y, z):
	self.parts = parts
	self.where = x, y, z
	self.comp = comp
	self.var = var

    def apply(self):
	x, y, z = self.where
	v = self.comp[self.var]
	
	glPushMatrix()
	glScalef(x*v, y*v, z*v)

    def unapply(self):
	glPopMatrix()


class HalRotate(Collection):
    def __init__(self, parts, comp, var, th, x, y, z):
	self.parts = parts
	self.where = th, x, y, z
	self.comp = comp
	self.var = var

    def apply(self):
	th, x, y, z = self.where
	glPushMatrix()
	glRotatef(th * self.comp[self.var], x, y, z)

    def unapply(self):
	glPopMatrix()


class Rotate(Collection):
    def __init__(self, parts, th, x, y, z):
	self.parts = parts
	self.where = th, x, y, z

    def apply(self):
	th, x, y, z = self.where
	glPushMatrix()
	glRotatef(th, x, y, z)

    def unapply(self):
	glPopMatrix()

# give endpoint X values and radii
# resulting cylinder is on the X axis
class CylinderX:
    def __init__(self, x1, r1, x2, r2):
	self.coords = x1, r1, x2, r2
	self.q = gluNewQuadric()

    def draw(self):
	x1, r1, x2, r2 = self.coords
	if x1 > x2:
	    tmp = x1
	    x1 = x2
	    x2 = tmp
	    tmp = r1
	    r1 = r2
	    r2 = tmp
	glPushMatrix()
	# GL creates cylinders along Z, so need to rotate
	z1 = x1
	z2 = x2
	glRotatef(90,0,1,0)
	# need to translate the whole thing to z1
	glTranslatef(0,0,z1)
	# the cylinder starts out at Z=0
	gluCylinder(self.q, r1, r2, z2-z1, 32, 1)
	# bottom cap
	glRotatef(180,1,0,0)
	gluDisk(self.q, 0, r1, 32, 1)
	glRotatef(180,1,0,0)
	# the top cap needs flipped and translated
	glPushMatrix()
	glTranslatef(0,0,z2-z1)
	gluDisk(self.q, 0, r2, 32, 1)
	glPopMatrix()
	glPopMatrix()

# give endpoint Y values and radii
# resulting cylinder is on the Y axis
class CylinderY:
    def __init__(self, y1, r1, y2, r2):
	self.coords = y1, r1, y2, r2
	self.q = gluNewQuadric()

    def draw(self):
	y1, r1, y2, r2 = self.coords
	if y1 > y2:
	    tmp = y1
	    y1 = y2
	    y2 = tmp
	    tmp = r1
	    r1 = r2
	    r2 = tmp
	glPushMatrix()
	# GL creates cylinders along Z, so need to rotate
	z1 = y1
	z2 = y2
	glRotatef(90,1,0,0)
	# need to translate the whole thing to z1
	glTranslatef(0,0,z1)
	# the cylinder starts out at Z=0
	gluCylinder(self.q, r1, r2, z2-z1, 32, 1)
	# bottom cap
	glRotatef(180,1,0,0)
	gluDisk(self.q, 0, r1, 32, 1)
	glRotatef(180,1,0,0)
	# the top cap needs flipped and translated
	glPushMatrix()
	glTranslatef(0,0,z2-z1)
	gluDisk(self.q, 0, r2, 32, 1)
	glPopMatrix()
	glPopMatrix()

# give endpoint Z values and radii
# resulting cylinder is on the Z axis
class CylinderZ:
    def __init__(self, z1, r1, z2, r2):
	self.coords = z1, r1, z2, r2
	self.q = gluNewQuadric()

    def draw(self):
	z1, r1, z2, r2 = self.coords
	if z1 > z2:
	    tmp = z1
	    z1 = z2
	    z2 = tmp
	    tmp = r1
	    r1 = r2
	    r2 = tmp
	# need to translate the whole thing to z1
	glPushMatrix()
	glTranslatef(0,0,z1)
	# the cylinder starts out at Z=0
	gluCylinder(self.q, r1, r2, z2-z1, 32, 1)
	# bottom cap
	glRotatef(180,1,0,0)
	gluDisk(self.q, 0, r1, 32, 1)
	glRotatef(180,1,0,0)
	# the top cap needs flipped and translated
	glPushMatrix()
	glTranslatef(0,0,z2-z1)
	gluDisk(self.q, 0, r2, 32, 1)
	glPopMatrix()
	glPopMatrix()

# give center and radius
class Sphere:
    def __init__(self, x, y, z, r):
	self.coords = x, y, z, r
	self.q = gluNewQuadric()

    def draw(self):
	x, y, z, r = self.coords
	# need to translate the whole thing to x,y,z
	glPushMatrix()
	glTranslatef(x,y,z)
	# the cylinder starts out at the origin
	gluSphere(self.q, r, 32, 16)
	glPopMatrix()

# six coordinate version - specify each side of the box
class Box:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.coords = x1, y1, z1, x2, y2, z2

    def draw(self):
        x1, y1, z1, x2, y2, z2 = self.coords
        if x1 > x2:
	    tmp = x1
	    x1 = x2
	    x2 = tmp
        if y1 > y2:
	    tmp = y1
	    y1 = y2
	    y2 = tmp
        if z1 > z2:
	    tmp = z1
	    z1 = z2
	    z2 = tmp

        glBegin(GL_QUADS)
	# bottom face
        glNormal3f(0,0,1)
        glVertex3f(x2, y1, z1)
        glVertex3f(x1, y1, z1)
        glVertex3f(x1, y2, z1)
        glVertex3f(x2, y2, z1)
	# positive X face
        glNormal3f(1,0,0)
        glVertex3f(x2, y1, z1)
        glVertex3f(x2, y2, z1)
        glVertex3f(x2, y2, z2)
        glVertex3f(x2, y1, z2)
	# positive Y face
        glNormal3f(0,1,0)
        glVertex3f(x1, y2, z1)
        glVertex3f(x1, y2, z2)
        glVertex3f(x2, y2, z2)
        glVertex3f(x2, y2, z1)
	# negative Y face
        glNormal3f(0,-1,0)
        glVertex3f(x2, y1, z2)
        glVertex3f(x1, y1, z2)
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y1, z1)
	# negative X face
        glNormal3f(-1,0,0)
        glVertex3f(x1, y1, z1)
        glVertex3f(x1, y1, z2)
        glVertex3f(x1, y2, z2)
        glVertex3f(x1, y2, z1)
	# top face
        glNormal3f(0,0,-1)
        glVertex3f(x1, y2, z2)
        glVertex3f(x1, y1, z2)
        glVertex3f(x2, y1, z2)
        glVertex3f(x2, y2, z2)
        glEnd()

# specify the width in X and Y, and the height in Z
# the box is centered on the origin
class BoxCentered(Box):
    def __init__(self, xw, yw, zw):
        self.coords = -xw/2.0, -yw/2.0, -zw/2.0, xw/2.0, yw/2.0, zw/2.0

# specify the width in X and Y, and the height in Z
# the box is centered in X and Y, and runs from Z=0 up
# (or down) to the specified Z value
class BoxCenteredXY(Box):
    def __init__(self, xw, yw, zw):
        self.coords = -xw/2.0, -yw/2.0, 0, xw/2.0, yw/2.0, zw

# capture current transformation matrix
# note that this tranforms from the current coordinate system
# to the viewport system, NOT to the world system
class Capture:
    def __init__(self):
	self.t = []

    def capture(self):
	self.t = glGetDoublev(GL_MODELVIEW_MATRIX)

# function to invert a transform matrix
# based on http://steve.hollasch.net/cgindex/math/matrix/afforthinv.c
# with simplifications since we don't do scaling

# This function inverts a 4x4 matrix that is affine and orthogonal.  In
# other words, the perspective components are [0 0 0 1], and the basis
# vectors are orthogonal to each other.  In addition, the matrix must
# not do scaling

def invert(src):
	# make a copy
	inv=src[:]
	# The inverse of the upper 3x3 is the transpose (since the basis
	# vectors are orthogonal to each other.
	inv[1],inv[4] = inv[4],inv[1]
	inv[2],inv[8] = inv[8],inv[2]
	inv[6],inv[9] = inv[9],inv[6]
	# The inverse of the translation component is just the negation
	# of the translation after dotting with the new upper3x3 rows. */	
	inv[12] = -(src[12]*inv[0] + src[13]*inv[4] + src[14]*inv[8])
	inv[13] = -(src[12]*inv[1] + src[13]*inv[5] + src[14]*inv[9])
	inv[14] = -(src[12]*inv[2] + src[13]*inv[6] + src[14]*inv[10])
	return inv

class O(rs274.OpenGLTk.Opengl):
    def __init__(self, *args, **kw):
        rs274.OpenGLTk.Opengl.__init__(self, *args, **kw)
        self.r_back = self.g_back = self.b_back = 0
        self.bind('<Button-4>', self.zoomin)
        self.bind('<Button-5>', self.zoomout)
	#self.q1 = gluNewQuadric()
	#self.q2 = gluNewQuadric()
	#self.q3 = gluNewQuadric()
	self.plotdata = []
	self.plotlen = 4000

    def zoomin(self, event):
        self.distance = self.distance / 1.1
        self.tkRedraw()

    def zoomout(self, event):
        self.distance = self.distance * 1.1
        self.tkRedraw()

    def basic_lighting(self):
        self.activate()
        glLightfv(GL_LIGHT0, GL_POSITION, (1, -1, .5, 0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (.2,.2,.2,0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (.6,.6,.4,0))
        glLightfv(GL_LIGHT0+1, GL_POSITION, (-1, -1, .5, 0))
        glLightfv(GL_LIGHT0+1, GL_AMBIENT, (.0,.0,.0,0))
        glLightfv(GL_LIGHT0+1, GL_DIFFUSE, (.0,.0,.4,0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (1,1,1,0))
	glEnable(GL_CULL_FACE)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT0+1)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def redraw(self, *args):
        if self.winfo_width() == 1: return
        self.model.traverse()
	# current coords: world
	# the matrices tool2view, work2view, and world2view
	# transform from tool/work/world coords to viewport coords
	# if we want to draw in tool coords, we need to do
	# "tool -> view -> world" (since the current frame is world)
	# and if we want to draw in work coords, we need
	# "work -> view -> world".  For both, we need to invert
	# the world2view matrix to do the second step
	view2world = invert(self.world2view.t)
	# likewise, for backplot, we want to transform the tooltip
	# position from tool coords (where it is [0,0,0]) to work
	# coords, so we need tool -> view -> work
	# so lets also invert the work2view matrix
	view2work = invert(self.work2view.t)

	# since backplot lines only need vertexes, not orientation,
	# and the tooltip is at the origin, getting the tool coords
	# is easy
	tx, ty, tz = self.tool2view.t[12:15]
	# now we have to transform them to the work frame
	wx = tx*view2work[0]+ty*view2work[4]+tz*view2work[8]+view2work[12]
	wy = tx*view2work[1]+ty*view2work[5]+tz*view2work[9]+view2work[13]
	wz = tx*view2work[2]+ty*view2work[6]+tz*view2work[10]+view2work[14]
	# wx, wy, wz are the values to use for backplot
	# so we save them in a buffer
        if len(self.plotdata) == self.plotlen:
	    del self.plotdata[:self.plotlen / 10]
	point = [ wx, wy, wz ]
	if not self.plotdata or point != self.plotdata[-1]:
	    self.plotdata.append(point)

	# now lets draw something in the tool coordinate system
	#glPushMatrix()
	# matrixes take effect in reverse order, so the next
	# two lines do "tool -> view -> world"
	#glMultMatrixd(view2world)
	#glMultMatrixd(self.tool2view.t)

	# do drawing here
	# cylinder normally goes to +Z, we want it down
	#glTranslatef(0,0,-60)
	#gluCylinder(self.q1, 20, 20, 60, 32, 16)

	# back to world coords
	#glPopMatrix()
	
	
	# we can also draw in the work coord system
	glPushMatrix()
	# "work -> view -> world"
	glMultMatrixd(view2world)
	glMultMatrixd(self.work2view.t)
	# now we can draw in work coords, and whatever we draw
	# will move with the work, (if the work is attached to
	# a table or indexer or something that moves with
	# respect to the world

	# just a test object, sitting on the table
	#gluCylinder(self.q2, 40, 20, 60, 32, 16)

	# draw backplot
	glDisable(GL_LIGHTING)
        glBegin(GL_LINE_STRIP)
	for p in self.plotdata:
	    glVertex3f(*p)
	glEnd()
	glEnable(GL_LIGHTING)

	# back to world again
	glPopMatrix()


def main(model, tool, work, size=10 ):
    app = Tkinter.Tk()

    t = O(app, double=1, depth=1)

    # need to capture the world coordinate system
    world = Capture()

    t.model = Collection([model, world])
    t.distance = size * 3
    t.near = size * 0.01
    t.far = size * 10.0
    t.tool2view = tool
    t.world2view = world
    t.work2view = work

    t.pack(fill="both", expand=1)

    def update():
	t.tkRedraw()
	t.after(100, update)
    update()
    try:
	app.mainloop()
    except KeyboardInterrupt:
	raise SystemExit
