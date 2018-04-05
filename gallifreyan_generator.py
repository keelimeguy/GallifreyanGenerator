import svgwrite
import argparse
import math
import re

class Gallifreyan:
    double_consonants = ['Th', 'Ph', 'Wh', 'Gh',
                         'th', 'ph', 'wh', 'gh',
                         'tH', 'pH', 'wH', 'gH',
                         'TH', 'PH', 'WH', 'GH',
                         'Ch', 'Sh', 'Qu', 'Ng',
                         'ch', 'sh', 'qu', 'ng',
                         'cH', 'sH', 'qU', 'nG',
                         'CH', 'SH', 'QU', 'NG']
    consonants = ['B', 'J', 'T', 'K', 'Y', 'D', 'L',
                  'b', 'j', 't', 'k', 'y', 'd', 'l',
                  'R', 'Z', 'C', 'Q', 'G', 'N', 'V',
                  'r', 'z', 'c', 'q', 'g', 'n', 'v',
                  'H', 'P', 'W', 'X', 'F', 'M', 'S',
                  'h', 'p', 'w', 'x', 'f', 'm', 's']
    vowels = ['A', 'E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u']
    punctuation = ['.', ',', ';', '?', '!', ':', '\"', '\'', '-']
    scale = 10

    class Punctuation:
        def __init__(self, text):
            self._text = text

        def __str__(self):
            return '\"'+self._text+'\"'
        __repr__ = __str__

        def precompile(self):
            self._r = Gallifreyan.scale/2
            self._radj = self._r/math.sqrt(2)
            return self._radj, self._r

        def compile(self, x, y, R, xo, yo, angle, dwg):
            dangle = 1.2*self._r*math.pi/(2*math.sqrt(2)*R)
            xs=R*math.cos(angle+dangle)+xo
            ys=-R*math.sin(angle+dangle)+yo
            xe=R*math.cos(angle-dangle)+xo
            ye=-R*math.sin(angle-dangle)+yo

            # Circle
            if self._text == '.':
                dwg.add(dwg.circle((x, y), self._r, stroke='black', fill='none'))

            # Fill Circle
            elif self._text == ',':
                dwg.add(dwg.circle((x, y), self._r, stroke='black', fill='black'))

            # Double Circle
            elif self._text == ':':
                dwg.add(dwg.circle((x, y), self._r, stroke='black', fill='none'))
                dwg.add(dwg.circle((x, y), self._r*.5, stroke='black', fill='none'))

            # 1 Circle outside
            elif self._text == ';':
                dwg.add(dwg.circle((x+(self._r)*math.cos(angle), y-(self._r)*math.sin(angle)), self._r/2, stroke='black', fill='black'))

            # 2 Circles outside
            elif self._text == '?':
                dwg.add(dwg.circle((xo+(R+self._r)*math.cos(angle+dangle*.5), yo-(R+self._r)*math.sin(angle+dangle*.5)), self._r/2, stroke='black', fill='black'))
                dwg.add(dwg.circle((xo+(R+self._r)*math.cos(angle-dangle*.5), yo-(R+self._r)*math.sin(angle-dangle*.5)), self._r/2, stroke='black', fill='black'))

            # 3 Circles outside
            elif self._text == '!':
                dwg.add(dwg.circle((x+(self._r)*math.cos(angle), y-(self._r)*math.sin(angle)), self._r/2, stroke='black', fill='black'))
                dwg.add(dwg.circle((xo+(R+self._r)*math.cos(angle+dangle), yo-(R+self._r)*math.sin(angle+dangle)), self._r/2, stroke='black', fill='black'))
                dwg.add(dwg.circle((xo+(R+self._r)*math.cos(angle-dangle), yo-(R+self._r)*math.sin(angle-dangle)), self._r/2, stroke='black', fill='black'))

            else:
                print('Warning: {} not yet implemented!'.format(self._text))

            # dwg.add(dwg.text(self._text, (x, y)))
            return self._radj, self._r

    class Sound(Punctuation):
        def precompile(self):
            self._r = Gallifreyan.scale*2
            self._radj = self._r/math.sqrt(2)
            return self._radj, self._r

        def compile(self, x, y, R, xo, yo, angle, dwg):
            dangle = self._r*math.pi/(2*math.sqrt(2)*R)
            xs=R*math.cos(angle+dangle)+xo
            ys=-R*math.sin(angle+dangle)+yo
            xe=R*math.cos(angle-dangle)+xo
            ye=-R*math.sin(angle-dangle)+yo
            combos = [c+v for v in Gallifreyan.vowels for c in Gallifreyan.consonants+Gallifreyan.double_consonants]

            half_circle_list = [c+v for v in ['a', 'e', 'i', 'o', 'u'] for c in ['t', 'wh', 'sh', 'r', 'v', 'w', 's']]+['t', 'wh', 'sh', 'r', 'v', 'w', 's']
            circle_partial_list = [c+v for v in ['a', 'e', 'i', 'o', 'u'] for c in ['b', 'ch', 'd', 'g', 'h', 'f']]+['b', 'ch', 'd', 'g', 'h', 'f']
            circle_list = [c+v for v in ['a', 'e', 'i', 'o', 'u'] for c in ['th', 'gh', 'y', 'z', 'q', 'qu', 'x', 'ng']]+['th', 'gh', 'y', 'z', 'q', 'qu', 'x', 'ng']
            circle_inside_list = [c+v for v in ['a', 'e', 'i', 'o', 'u'] for c in ['j', 'ph', 'k', 'l', 'c', 'n', 'p', 'm']]+['j', 'ph', 'k', 'l', 'c', 'n', 'p', 'm']

            one_dot_list = [c+v for v in ['a', 'e', 'i', 'o', 'u'] for c in ['ph', 'wh', 'gh']]+['ph', 'wh', 'gh']
            two_dots_list = [c+v for v in ['a', 'e', 'i', 'o', 'u'] for c in ['ch', 'k', 'sh', 'y']]+['ch', 'k', 'sh', 'y']
            three_dots_list = [c+v for v in ['a', 'e', 'i', 'o', 'u'] for c in ['d', 'l', 'r', 'z']]+['d', 'l', 'r', 'z']
            four_dots_list = [c+v for v in ['a', 'e', 'i', 'o', 'u'] for c in ['c', 'q']]+['c', 'q']
            one_line_list = [c+v for v in ['a', 'e', 'i', 'o', 'u'] for c in ['g', 'n', 'v', 'qu']]+['g', 'n', 'v', 'qu']
            two_lines_list = [c+v for v in ['a', 'e', 'i', 'o', 'u'] for c in ['h', 'p', 'w', 'x']]+['h', 'p', 'w', 'x']
            three_lines_list = [c+v for v in ['a', 'e', 'i', 'o', 'u'] for c in ['f', 'm', 's', 'ng']]+['f', 'm', 's', 'ng']

            inward_lines = []

            if self._text.lower() == 'a':
                dwg.add(dwg.circle((x+Gallifreyan.scale*math.cos(angle), y-Gallifreyan.scale*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
            elif self._text.lower() == 'e':
                dwg.add(dwg.circle((x, y), Gallifreyan.scale, stroke='black', fill='none'))
            elif self._text.lower() == 'i':
                dwg.add(dwg.circle((x, y), Gallifreyan.scale, stroke='black', fill='none'))
                newxoff = Gallifreyan.scale*math.cos(angle)
                newyoff = Gallifreyan.scale*math.sin(angle)
                inward_lines.append((x-newxoff, y+newyoff, angle))
                # dwg.add(dwg.line((x-newxoff, y+newyoff), (xo, yo), stroke='black'))
            elif self._text.lower() == 'o':
                dwg.add(dwg.circle((x-Gallifreyan.scale*math.cos(angle), y+Gallifreyan.scale*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
            elif self._text.lower() == 'u':
                dwg.add(dwg.circle((x, y), Gallifreyan.scale, stroke='black', fill='none'))
                newxoff = Gallifreyan.scale*math.cos(angle)
                newyoff = Gallifreyan.scale*math.sin(angle)
                dwg.add(dwg.line((x+newxoff, y-newyoff), (x+10*newxoff, y-10*newyoff), stroke='black'))

            # Half circle crater
            elif self._text.lower() in half_circle_list:
                dwg.add(dwg.path("M{},{} a1,1 0 0,{} {},{} a1,1 0 0,{} {},{}".format(xs, ys, 0, xe-xs, ye-ys, 0, xs-xe, ys-ye), fill='white', stroke='none'))
                dwg.add(dwg.path("M{},{} a1,1 0 0,{} {},{}".format(xs, ys, 0, xe-xs, ye-ys), fill='white', stroke='black'))
                if self._text.lower() in one_dot_list:
                    dwg.add(dwg.circle((x-(self._r-Gallifreyan.scale/2)*math.cos(angle), y+(self._r-Gallifreyan.scale/2)*math.sin(angle)), Gallifreyan.scale/4, stroke='none', fill='black'))
                elif self._text.lower() in two_dots_list:
                    dwg.add(dwg.circle((xo+(R-self._r/2)*math.cos(angle+dangle*.5), yo-(R-self._r/2)*math.sin(angle+dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((xo+(R-self._r/2)*math.cos(angle-dangle*.5), yo-(R-self._r/2)*math.sin(angle-dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                elif self._text.lower() in three_dots_list:
                    dwg.add(dwg.circle((x-(self._r-Gallifreyan.scale/2)*math.cos(angle), y+(self._r-Gallifreyan.scale/2)*math.sin(angle)), Gallifreyan.scale/4, stroke='none', fill='black'))
                    dwg.add(dwg.circle((xo+(R-self._r/2)*math.cos(angle+dangle*.5), yo-(R-self._r/2)*math.sin(angle+dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((xo+(R-self._r/2)*math.cos(angle-dangle*.5), yo-(R-self._r/2)*math.sin(angle-dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                elif self._text.lower() in four_dots_list:
                    pass
                elif self._text.lower() in one_line_list:
                    newx = (xs+xe)/2 - (self._r*math.pi/(2*math.sqrt(2)))*math.cos(angle+math.pi/4)
                    newy = (ys+ye)/2 + (self._r*math.pi/(2*math.sqrt(2)))*math.sin(angle+math.pi/4)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                elif self._text.lower() in two_lines_list:
                    newx = (xs+xe)/2 - (self._r*math.pi/(2*math.sqrt(2)))*math.cos(angle+math.pi/4)
                    newy = (ys+ye)/2 + (self._r*math.pi/(2*math.sqrt(2)))*math.sin(angle+math.pi/4)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                    newx = (xs+xe)/2 - (self._r*math.pi/(2*math.sqrt(2)))*math.cos(angle-math.pi/4)
                    newy = (ys+ye)/2 + (self._r*math.pi/(2*math.sqrt(2)))*math.sin(angle-math.pi/4)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                elif self._text.lower() in three_lines_list:
                    newx = (xs+xe)/2 - (self._r*math.pi/(2*math.sqrt(2)))*math.cos(angle+math.pi/3)
                    newy = (ys+ye)/2 + (self._r*math.pi/(2*math.sqrt(2)))*math.sin(angle+math.pi/3)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                    newx = (xs+xe)/2 - (self._r*math.pi/(2*math.sqrt(2)))*math.cos(angle+math.pi/5)
                    newy = (ys+ye)/2 + (self._r*math.pi/(2*math.sqrt(2)))*math.sin(angle+math.pi/5)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                    newx = (xs+xe)/2 - (self._r*math.pi/(2*math.sqrt(2)))*math.cos(angle-math.pi/4)
                    newy = (ys+ye)/2 + (self._r*math.pi/(2*math.sqrt(2)))*math.sin(angle-math.pi/4)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))

                if self._text.lower()[-1] == 'a':
                    dwg.add(dwg.circle((x+Gallifreyan.scale*math.cos(angle), y-Gallifreyan.scale*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
                elif self._text.lower()[-1] == 'e':
                    dwg.add(dwg.circle((x, y), Gallifreyan.scale/2, stroke='black', fill='none'))
                elif self._text.lower()[-1] == 'i':
                    dwg.add(dwg.circle((x, y), Gallifreyan.scale/2, stroke='black', fill='none'))
                    newxoff = Gallifreyan.scale/2*math.cos(angle)
                    newyoff = Gallifreyan.scale/2*math.sin(angle)
                    inward_lines.append((x-newxoff, y+newyoff, angle))
                    # dwg.add(dwg.line((x-newxoff, y+newyoff), (xo, yo), stroke='black'))
                elif self._text.lower()[-1] == 'o':
                    dwg.add(dwg.circle((x-(self._r+Gallifreyan.scale/2)*math.cos(angle), y+(self._r+Gallifreyan.scale/2)*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
                elif self._text.lower()[-1] == 'u':
                    dwg.add(dwg.circle((x, y), Gallifreyan.scale/2, stroke='black', fill='none'))
                    newxoff = Gallifreyan.scale/2*math.cos(angle)
                    newyoff = Gallifreyan.scale/2*math.sin(angle)
                    dwg.add(dwg.line((x+newxoff, y-newyoff), (x+10*newxoff, y-10*newyoff), stroke='black'))

            # Circle partial inside
            elif self._text.lower() in circle_partial_list:
                xoff = 0.8*self._r*math.cos(angle)
                yoff = 0.8*self._r*math.sin(angle)
                dwg.add(dwg.circle((x - xoff, y + yoff), .9*self._r, stroke='black', fill='none'))
                dwg.add(dwg.circle((x + xoff, y - yoff), self._r, stroke='none', fill='white'))
                if self._text.lower() in one_dot_list:
                    pass
                elif self._text.lower() in two_dots_list:
                    dwg.add(dwg.circle((xo-xoff+(R-self._r/2)*math.cos(angle+dangle*.5), yo+yoff-(R-self._r/2)*math.sin(angle+dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((xo-xoff+(R-self._r/2)*math.cos(angle-dangle*.5), yo+yoff-(R-self._r/2)*math.sin(angle-dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                elif self._text.lower() in three_dots_list:
                    dwg.add(dwg.circle((x-xoff-(.5*self._r-Gallifreyan.scale/4)*math.cos(angle), y+yoff+(.5*self._r-Gallifreyan.scale/4)*math.sin(angle)), Gallifreyan.scale/4, stroke='none', fill='black'))
                    dwg.add(dwg.circle((xo-xoff+(R-self._r/2)*math.cos(angle+dangle*.5), yo+yoff-(R-self._r/2)*math.sin(angle+dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((xo-xoff+(R-self._r/2)*math.cos(angle-dangle*.5), yo+yoff-(R-self._r/2)*math.sin(angle-dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                elif self._text.lower() in four_dots_list:
                    pass
                elif self._text.lower() in one_line_list:
                    newx = x-xoff - .9*self._r*math.cos(angle+math.pi/4)
                    newy = y+yoff + .9*self._r*math.sin(angle+math.pi/4)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                elif self._text.lower() in two_lines_list:
                    newx = x-xoff - .9*self._r*math.cos(angle+math.pi/4)
                    newy = y+yoff + .9*self._r*math.sin(angle+math.pi/4)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                    newx = x-xoff - .9*self._r*math.cos(angle-math.pi/4)
                    newy = y+yoff + .9*self._r*math.sin(angle-math.pi/4)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                elif self._text.lower() in three_lines_list:
                    newx = x-xoff - .9*self._r*math.cos(angle+math.pi/3)
                    newy = y+yoff + .9*self._r*math.sin(angle+math.pi/3)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                    newx = x-xoff - .9*self._r*math.cos(angle+math.pi/5)
                    newy = y+yoff + .9*self._r*math.sin(angle+math.pi/5)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                    newx = x-xoff - .9*self._r*math.cos(angle-math.pi/4)
                    newy = y+yoff + .9*self._r*math.sin(angle-math.pi/4)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))

                if self._text.lower()[-1] == 'a':
                    dwg.add(dwg.circle((x+Gallifreyan.scale*math.cos(angle), y-Gallifreyan.scale*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
                elif self._text.lower()[-1] == 'e':
                    dwg.add(dwg.circle((x-xoff, y+yoff), Gallifreyan.scale/2, stroke='black', fill='none'))
                elif self._text.lower()[-1] == 'i':
                    dwg.add(dwg.circle((x-xoff, y+yoff), Gallifreyan.scale/2, stroke='black', fill='none'))
                    newxoff = Gallifreyan.scale/2*math.cos(angle)
                    newyoff = Gallifreyan.scale/2*math.sin(angle)
                    inward_lines.append((x-xoff-newxoff, y+yoff+newyoff, angle))
                    # dwg.add(dwg.line((x-xoff-newxoff, y+yoff+newyoff), (xo, yo), stroke='black'))
                elif self._text.lower()[-1] == 'o':
                    dwg.add(dwg.circle((x-xoff-(self._r*.9)*math.cos(angle), y+yoff+(self._r*.9)*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
                elif self._text.lower()[-1] == 'u':
                    dwg.add(dwg.circle((x-xoff, y+yoff), Gallifreyan.scale/2, stroke='black', fill='none'))
                    newxoff = Gallifreyan.scale/2*math.cos(angle)
                    newyoff = Gallifreyan.scale/2*math.sin(angle)
                    dwg.add(dwg.line((x-xoff+newxoff, y+yoff-newyoff), (x-xoff+10*newxoff, y+yoff-10*newyoff), stroke='black'))

            # Circle
            elif self._text.lower() in circle_list:
                dwg.add(dwg.circle((x, y), self._r, stroke='black', fill='none'))
                if self._text.lower() in one_dot_list:
                    dwg.add(dwg.circle((x+(self._r/2)*math.cos(angle), y-(self._r/2)*math.sin(angle)), Gallifreyan.scale/4, stroke='none', fill='black'))
                elif self._text.lower() in two_dots_list:
                    dwg.add(dwg.circle((xo+(R-self._r/2)*math.cos(angle+dangle*.5), yo-(R-self._r/2)*math.sin(angle+dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((xo+(R-self._r/2)*math.cos(angle-dangle*.5), yo-(R-self._r/2)*math.sin(angle-dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                elif self._text.lower() in three_dots_list:
                    dwg.add(dwg.circle((x-(self._r/2)*math.cos(angle), y+(self._r/2)*math.sin(angle)), Gallifreyan.scale/4, stroke='none', fill='black'))
                    dwg.add(dwg.circle((xo+(R-self._r/2)*math.cos(angle+dangle*.5), yo-(R-self._r/2)*math.sin(angle+dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((xo+(R-self._r/2)*math.cos(angle-dangle*.5), yo-(R-self._r/2)*math.sin(angle-dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                elif self._text.lower() in one_line_list:
                    newx = x - self._r*math.cos(angle+math.pi/4)
                    newy = y + self._r*math.sin(angle+math.pi/4)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                elif self._text.lower() in four_dots_list:
                    dwg.add(dwg.circle((xo+(R-self._r/2)*math.cos(angle+dangle*.5), yo-(R-self._r/2)*math.sin(angle+dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((xo+(R-self._r/2)*math.cos(angle-dangle*.5), yo-(R-self._r/2)*math.sin(angle-dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((xo+(R-self._r/2)*math.cos(angle+dangle), yo-(R-self._r/2)*math.sin(angle+dangle)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((xo+(R-self._r/2)*math.cos(angle-dangle), yo-(R-self._r/2)*math.sin(angle-dangle)), Gallifreyan.scale/4, stroke='black', fill='black'))
                elif self._text.lower() in two_lines_list:
                    newx = x - self._r*math.cos(angle+math.pi/4)
                    newy = y + self._r*math.sin(angle+math.pi/4)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                    newx = x - self._r*math.cos(angle-math.pi/4)
                    newy = y + self._r*math.sin(angle-math.pi/4)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                elif self._text.lower() in three_lines_list:
                    newx = x - self._r*math.cos(angle+math.pi/3)
                    newy = y + self._r*math.sin(angle+math.pi/3)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                    newx = x - self._r*math.cos(angle+math.pi/5)
                    newy = y + self._r*math.sin(angle+math.pi/5)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))
                    newx = x - self._r*math.cos(angle-math.pi/4)
                    newy = y + self._r*math.sin(angle-math.pi/4)
                    dwg.add(dwg.line((newx, newy), (xo, yo), stroke='black'))

                if self._text.lower()[-1] == 'a':
                    dwg.add(dwg.circle((x+Gallifreyan.scale*math.cos(angle), y-Gallifreyan.scale*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
                elif self._text.lower()[-1] == 'e':
                    dwg.add(dwg.circle((x, y), Gallifreyan.scale/2, stroke='black', fill='none'))
                elif self._text.lower()[-1] == 'i':
                    dwg.add(dwg.circle((x, y), Gallifreyan.scale/2, stroke='black', fill='none'))
                    newxoff = Gallifreyan.scale/2*math.cos(angle)
                    newyoff = Gallifreyan.scale/2*math.sin(angle)
                    inward_lines.append((x-newxoff, y+newyoff, angle))
                    # dwg.add(dwg.line((x-newxoff, y+newyoff), (xo, yo), stroke='black'))
                elif self._text.lower()[-1] == 'o':
                    dwg.add(dwg.circle((x-(self._r)*math.cos(angle), y+(self._r)*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
                elif self._text.lower()[-1] == 'u' and self._text.lower() != 'qu':
                    dwg.add(dwg.circle((x, y), Gallifreyan.scale/2, stroke='black', fill='none'))
                    newxoff = Gallifreyan.scale/2*math.cos(angle)
                    newyoff = Gallifreyan.scale/2*math.sin(angle)
                    dwg.add(dwg.line((x+newxoff, y-newyoff), (x+10*newxoff, y-10*newyoff), stroke='black'))

            # Circle inside
            elif self._text.lower() in circle_inside_list:
                newx = x-(self._r*1.1)*math.cos(angle)
                newy = y+(self._r*1.1)*math.sin(angle)
                newxo = xo-(self._r*1.1)*math.cos(angle)
                newyo = yo+(self._r*1.1)*math.sin(angle)
                dwg.add(dwg.circle((newx, newy), self._r, stroke='black', fill='none'))
                if self._text.lower() in one_dot_list:
                    dwg.add(dwg.circle((newx+(self._r/2)*math.cos(angle), newy-(self._r/2)*math.sin(angle)), Gallifreyan.scale/4, stroke='none', fill='black'))
                elif self._text.lower() in two_dots_list:
                    dwg.add(dwg.circle((newxo+(R-self._r/2)*math.cos(angle+dangle*.5), newyo-(R-self._r/2)*math.sin(angle+dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((newxo+(R-self._r/2)*math.cos(angle-dangle*.5), newyo-(R-self._r/2)*math.sin(angle-dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                elif self._text.lower() in three_dots_list:
                    dwg.add(dwg.circle((newx-(self._r/2)*math.cos(angle), newy+(self._r/2)*math.sin(angle)), Gallifreyan.scale/4, stroke='none', fill='black'))
                    dwg.add(dwg.circle((newxo+(R-self._r/2)*math.cos(angle+dangle*.5), newyo-(R-self._r/2)*math.sin(angle+dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((newxo+(R-self._r/2)*math.cos(angle-dangle*.5), newyo-(R-self._r/2)*math.sin(angle-dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                elif self._text.lower() in four_dots_list:
                    dwg.add(dwg.circle((newxo+(R-self._r/2)*math.cos(angle+dangle*.5), newyo-(R-self._r/2)*math.sin(angle+dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((newxo+(R-self._r/2)*math.cos(angle-dangle*.5), newyo-(R-self._r/2)*math.sin(angle-dangle*.5)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((newxo+(R-self._r/2)*math.cos(angle+dangle), newyo-(R-self._r/2)*math.sin(angle+dangle)), Gallifreyan.scale/4, stroke='black', fill='black'))
                    dwg.add(dwg.circle((newxo+(R-self._r/2)*math.cos(angle-dangle), newyo-(R-self._r/2)*math.sin(angle-dangle)), Gallifreyan.scale/4, stroke='black', fill='black'))
                elif self._text.lower() in one_line_list:
                    newxx = newx - self._r*math.cos(angle+math.pi/4)
                    newyy = newy + self._r*math.sin(angle+math.pi/4)
                    dwg.add(dwg.line((newxx, newyy), (xo, yo), stroke='black'))
                elif self._text.lower() in two_lines_list:
                    newxx = newx - self._r*math.cos(angle+math.pi/4)
                    newyy = newy + self._r*math.sin(angle+math.pi/4)
                    dwg.add(dwg.line((newxx, newyy), (xo, yo), stroke='black'))
                    newxx = newx - self._r*math.cos(angle-math.pi/4)
                    newyy = newy + self._r*math.sin(angle-math.pi/4)
                    dwg.add(dwg.line((newxx, newyy), (xo, yo), stroke='black'))
                elif self._text.lower() in three_lines_list:
                    newxx = newx - self._r*math.cos(angle+math.pi/3)
                    newyy = newy + self._r*math.sin(angle+math.pi/3)
                    dwg.add(dwg.line((newxx, newyy), (xo, yo), stroke='black'))
                    newxx = newx - self._r*math.cos(angle+math.pi/5)
                    newyy = newy + self._r*math.sin(angle+math.pi/5)
                    dwg.add(dwg.line((newxx, newyy), (xo, yo), stroke='black'))
                    newxx = newx - self._r*math.cos(angle-math.pi/4)
                    newyy = newy + self._r*math.sin(angle-math.pi/4)
                    dwg.add(dwg.line((newxx, newyy), (xo, yo), stroke='black'))

                if self._text.lower()[-1] == 'a':
                    dwg.add(dwg.circle((x+Gallifreyan.scale*math.cos(angle), y-Gallifreyan.scale*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
                elif self._text.lower()[-1] == 'e':
                    dwg.add(dwg.circle((x-(self._r*1.1)*math.cos(angle), y+(self._r*1.1)*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
                elif self._text.lower()[-1] == 'i':
                    dwg.add(dwg.circle((x-(self._r*1.1)*math.cos(angle), y+(self._r*1.1)*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
                    newxoff = Gallifreyan.scale/2*math.cos(angle)
                    newyoff = Gallifreyan.scale/2*math.sin(angle)
                    inward_lines.append((x-(self._r*1.1)*math.cos(angle)-newxoff, y+(self._r*1.1)*math.sin(angle)+newyoff, angle))
                    # dwg.add(dwg.line((x-(self._r*1.1)*math.cos(angle)-newxoff, y+(self._r*1.1)*math.sin(angle)+newyoff), (xo, yo), stroke='black'))
                elif self._text.lower()[-1] == 'o':
                    dwg.add(dwg.circle((x-2*(self._r)*math.cos(angle), y+2*(self._r)*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
                elif self._text.lower()[-1] == 'u':
                    dwg.add(dwg.circle((x-(self._r*1.1)*math.cos(angle), y+(self._r*1.1)*math.sin(angle)), Gallifreyan.scale/2, stroke='black', fill='none'))
                    newxoff = Gallifreyan.scale/2*math.cos(angle)
                    newyoff = Gallifreyan.scale/2*math.sin(angle)
                    dwg.add(dwg.line((x-(self._r*1.1)*math.cos(angle)+newxoff, y+(self._r*1.1)*math.sin(angle)-newyoff), (x-(self._r*1.1)*math.cos(angle)+10*newxoff, y+(self._r*1.1)*math.sin(angle)-10*newyoff), stroke='black'))

            else:
                print('Warning: {} not yet implemented!'.format(self._text))

            return inward_lines

    class Word:
        def __init__(self, text):
            self._text = text
            self._sounds = []
            combos = [c+v for v in Gallifreyan.vowels for c in Gallifreyan.double_consonants+Gallifreyan.consonants]
            for s in (re.compile('|'.join(['('+s+')' for s in combos+Gallifreyan.double_consonants])).split(text)):
                if s:
                    if s in Gallifreyan.double_consonants+combos:
                        self._sounds.append(Gallifreyan.Sound(s))
                    else:
                        for c in s:
                            if c in Gallifreyan.consonants+Gallifreyan.vowels:
                                self._sounds.append(Gallifreyan.Sound(c))
                            else:
                                print('Warning: {} not a valid character.'.format(c))

        def __str__(self):
            return '\"'+self._text+'\"'
        __repr__ = __str__

        def __len__(self):
            return len(self._sounds)

        def precompile(self):
            self._r = len(self._sounds)*(2 if len(self._sounds)>2 else 3)*Gallifreyan.scale/math.sqrt(2)
            self._radj = self._r/math.sqrt(2)
            return self._radj, self._r

        def compile(self, x, y, R, xo, yo, angle, dwg):
            inward_lines = []
            for sound in self._sounds:
                sound.precompile()
            if len(self._sounds) == 1:
                    inward_lines+=self._sounds[0].compile(x, y, R, xo, yo, angle, dwg)
            else:
                dwg.add(dwg.circle((x, y), self._r, stroke='black', fill='none'))
                for i in range(len(self._sounds)):
                    angle = i*2*math.pi/len(self._sounds)-math.pi/2
                    inward_lines+=self._sounds[i].compile(x+math.cos(angle)*self._r, y-math.sin(angle)*self._r, self._r, x, y, angle, dwg)

            i = 1
            inward_lines_leftover = list(range(len(inward_lines)))
            while len(inward_lines_leftover)>1:
                j = (i+int(len(inward_lines)/2))%len(inward_lines)
                if j not in inward_lines_leftover:
                    j=(j+1)%len(inward_lines)
                dwg.add(dwg.line(inward_lines[i][:2], inward_lines[j][:2], stroke='black'))
                inward_lines_leftover.remove(i)
                inward_lines_leftover.remove(j)
                i=(i+1)%len(inward_lines)
            if inward_lines_leftover:
                if len(self._sounds)==1:
                    xx,yy,aangle = inward_lines[inward_lines_leftover[0]]
                    dwg.add(dwg.line((xx, yy), (xo-(R)*math.cos(aangle),yo+(R)*math.sin(aangle)), stroke='black'))
                else:
                    xx,yy,aangle = inward_lines[inward_lines_leftover[0]]
                    dwg.add(dwg.line((xx, yy), (x-(self._r)*math.cos(aangle),y+(self._r)*math.sin(aangle)), stroke='black'))

            # dwg.add(dwg.text(self._text, (x, y)))
            return self._radj, self._r

    def __init__(self, text):
        self._text = text
        self._words = []
        for word in re.compile('('+'|'.join(['\\'+s for s in self.punctuation+[' ', '\n', '\t', '\r']])+')').split(text):
            if word in self.punctuation:
                self._words.append(self.Punctuation(word))
            elif word not in [' ', '\n', '\t', '\r', '']:
                self._words.append(self.Word(word))

    def __str__(self):
        return self._text
    __repr__ = __str__

    def words(self):
        return self._words

    def compile(self, dwg):
        R = 0
        for word in self._words:
            adj, r = word.precompile()
            R += r
        Rorig = R
        if len(self._words)>3:
            R /= math.sqrt(2)
        elif len(self._words)<3:
            R *= math.sqrt(2)*.8
        x = y = R*math.sqrt(2)
        angle = -math.pi/2
        for i in range(len(self._words)):
            # angle = i*2*math.pi/len(self._words)-math.pi/2
            if not (isinstance(self._words[i], self.Punctuation) or len(self._words[i])==1):
                self._words[i].compile(x+math.cos(angle)*(R-1.1*self._words[i]._r), y-math.sin(angle)*(R-1.1*self._words[i]._r), R, x, y, angle, dwg)
            angle += math.pi*(self._words[i]._r+(self._words[i+1]._r if i < len(self._words)-1 else 0))/(Rorig)
        if len(self._words)>1:
            dwg.add(dwg.circle((x, y), R, stroke='black', fill='none'))
        angle = -math.pi/2
        for i in range(len(self._words)):
            # angle = i*2*math.pi/len(self._words)-math.pi/2
            if isinstance(self._words[i], self.Punctuation) or len(self._words[i])==1:
                self._words[i].compile(x+math.cos(angle)*R, y-math.sin(angle)*R, R, x, y, angle, dwg)
            angle += math.pi*(self._words[i]._r+(self._words[i+1]._r if i < len(self._words)-1 else 0))/(Rorig)
        dwg.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert given text into Gallifreyan.')
    parser.add_argument('-t', '--text', default=None,
                        help='The text to convert.')
    parser.add_argument('-o', '--output', default="text.svg",
                        help='The output svg file.')
    args = parser.parse_args()

    if args.text == None:
        print('Try running with -h.')
        exit(0)

    g = Gallifreyan(args.text)
    print(g)
    print(g.words())
    dwg = svgwrite.Drawing(args.output, profile='tiny')
    g.compile(dwg)
