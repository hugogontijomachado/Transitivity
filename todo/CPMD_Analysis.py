import numpy as np
import matplotlib.pyplot as plt
import os
import math as mt

class bond:
    def __init__(self):
        self.bond_out = {}
        self.angle_out = {}
        self.bonds = []
        self.angles = []

    def run(self,atoms = [],bonds = [],angles = [],dir = False):
        if dir == False:
            file = 'TRAJEC.xyz'
        else:
            file = str(dir) + '\\TRAJEC.xyz'
        input = open(file,'r')

        self.bonds = bonds
        self.angles = angles

        for n in range(len(self.bonds)):
            self.bond_out[self.bonds[n][0]+'-'+self.bonds[n][1]] = []

        for n in range(len(self.angles)):
            self.angle_out[self.angles[n][0]+'-'+self.angles[n][1]+'-'+ self.angles[n][2]] = []

        atoms.append(('',0))

        for ln in input:
            if 'STEP:' in ln:
                atom_out = {}
                for n in range(len(atoms)-1):
                    for i in range(atoms[n][1]-atoms[n-1][1]):
                        line = input.readline()
                    atom_out[atoms[n][0]] = np.array([float(line.split()[1]), float(line.split()[2]), float(line.split()[3])])

                for n in range(len(self.bonds)):
                    bond = np.abs(np.sqrt(sum(np.power((atom_out[self.bonds[n][0]] - atom_out[self.bonds[n][1]]), 2))))
                    self.bond_out[self.bonds[n][0] +'-'+ self.bonds[n][1]].append(bond)

                for n in range(len(self.angles)):
                    AB = np.abs(np.sqrt(sum(np.power((atom_out[self.angles[n][0]] - atom_out[self.angles[n][1]]), 2))))
                    BC = np.abs(np.sqrt(sum(np.power((atom_out[self.angles[n][1]] - atom_out[self.angles[n][2]]), 2))))
                    AC = np.abs(np.sqrt(sum(np.power((atom_out[self.angles[n][0]] - atom_out[self.angles[n][2]]), 2))))
                    cosB = ( (AC*AC)-(AB*AB)-(BC*BC) )/(2*AB*BC)
                    angle = np.rad2deg(np.arccos(cosB))
                    self.angle_out[self.angles[n][0] + '-' + self.angles[n][1] + '-' + self.angles[n][2]].append(angle)

        if len(self.bonds) != 0:
            self.step = np.array([x for x in range(1,len(self.bond_out[self.bonds[0][0]+'-'+self.bonds[0][1]])+1)])
        else:
            self.step = np.array([x for x in range(1, len(self.angle_out[self.angles[0][0] + '-' + self.angles[0][1] + '-' + self.angles[0][2]]) + 1)])
        input.close()

    def plot(self,title = '',save='show',color_bond='none',color_angle='none',savename='none'):
        if savename == 'none':
            if len(self.angles) > 0 :
                savename = 'angles' + title + '.png'
            else:
                savename = 'bond'+ title +'.png'
        else:
            if len(self.angles) > 0 :
                savename = 'angles' + savename + '.png'
            else:
                savename = 'bond'+ savename +'.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)

        for n in range(len(self.bond_out)):
            ax.set_ylabel('Distance (Å)', fontsize='x-large')
            if color_bond == 'none':
                ax.plot(self.step*5*0.121*0.001, self.bond_out[self.bonds[n][0] +'-'+ self.bonds[n][1]], label=self.bonds[n][0] +'-'+ self.bonds[n][1])
            else:
                ax.plot(self.step*5*0.121*0.001, self.bond_out[self.bonds[n][0] + '-' + self.bonds[n][1]],color_bond[n],label=self.bonds[n][0] + '-' + self.bonds[n][1])
                #ax.plot(self.step, self.bond_out[self.bonds[n][0] + '-' + self.bonds[n][1]],color_bond[n], label=self.bonds[n][0] + '-' + self.bonds[n][1])

        for n in range(len(self.angle_out)):
            ax.set_ylabel('Angle (Degreeº)', fontsize='x-large')
            if color_angle == 'none':
                ax.plot(self.step*5*0.121*0.001, self.angle_out[self.angles[n][0]+'-'+self.angles[n][1]+'-'+ self.angles[n][2]], label=self.angles[n][0]+'-'+self.angles[n][1]+'-'+ self.angles[n][2])
            else:
                ax.plot(self.step*5*0.121*0.001, self.angle_out[self.angles[n][0]+'-'+self.angles[n][1]+'-'+ self.angles[n][2]],color_angle[n],label=self.angles[n][0]+'-'+self.angles[n][1]+'-'+ self.angles[n][2])

        ax.set_xlabel('Time (ps)', fontsize='x-large')
        ax.set_title(title, fontsize='x-large')
        plt.legend(loc='best')
        if save == 'show':
            plt.show()
        elif save=='save':
            plt.savefig(savename)
        plt.close(fig)

class adiabaticity:
    def __init__(self):
        self.Ekin = []
        self.Ec = []
        self.Eks = []
        self.step = []

    def run(self,dir = False):
        if dir == False:
            file = 'ENERGIES'
        else:
            file = str(dir) + '\\ENERGIES'

        input = open(file, 'r')

        for ln in input:
            self.step.append(float(ln[5:11]))
            self.Ekin.append(float(ln[11:23]))
            self.Ec.append(float(ln[50:68]))
            self.Eks.append(float(ln[32:50]))

        self.step = np.array(self.step)
        self.Ekin = np.array(self.Ekin)
        self.Ec = np.array(self.Ec)
        self.Eks = np.array(self.Eks)

    def plot(self,save='show',title='',color_e='darkblue',color_n = 'red',savename='none'):
        if savename == 'none':
            savename =  'AdiabaticityAnalysis_'+ title +'.png'
        else:
            savename = 'AdiabaticityAnalysis_'+ savename +'.png'

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.step*0.121*0.001, self.Ekin, color_e , label='Eletrônica')
        ax.plot(self.step*0.121*0.001, self.Ec - self.Eks, color_n, label='Nuclear')

        ax.set_title(title,fontsize='x-large')
        ax.set_xlabel('Time (ps)', fontsize='x-large')
        ax.set_ylabel('Energia cinética (Hartree)', fontsize='x-large')
        ax.legend(loc='best')
        if save == 'show':
            plt.show()
        elif save == 'save':
            fig.savefig(savename)
        plt.close(fig)

def frame2gjf(frame,dir = False):
    if dir == False:
        dir = 'TRAJEC'
        file = 'TRAJEC.xyz'
    else:
        file = str(dir) + '\\TRAJEC.xyz'
    input = open(file, 'r')
    out_txt = []
    for ln in input:
        if 'STEP:' in ln and ln.split()[1] == frame :
            for i in range(4):
                out_txt.append(input.readline())

    head = ['%chk=test.chk\n',
            '# opt pm6 freq=noraman\n\n',
            'Title\n\n',
            '0 2\n']
    out = open(dir + '_frame_'+frame+'.gjf', 'w')
    out.writelines(head)
    out.writelines(out_txt)
    out.writelines('\n\n')

class gjf2pov:
    def __init__(self):
        self.atom = {}
        self.coord = {}
        self.bond = {}

        self.raio_atom = {'H': '0.2',
                     'C': '0.325',
                     'N': '0.325',
                     'O': '0.325',
                     'F': '0.325',
                     'Cl': '0.325'}

        self.cor_atom = {'H': ' 0.745098, 0.745098, 0.745098 ',
                    'C': ' 0.466667, 0.466667, 0.466667 ',
                    'N': ' 0.631373, 0.631373, 1 ',
                    'O': ' 0.796078, 0, 0 ',
                    'F': ' 0.776471, 1, 0.0705882 ',
                    'Cl': '  0.266667, 1, 0.227451 ' }

        self.raio_bond = '0.1'
        self.cor_bond = ' 0.2 , 0.2 , 0.2 '
        self.raio_bond_ts = '0.03'
        self.step_ts = '3'
        self.cor_bond_ts = ' 0.3 , 0.3 , 0.3 '

    def Text(self, p):
        p = str(float(p) * 9361.04)
        head_txt = [
            #                '#version 3.7;\n',
            'global_settings {\n',
            '    assumed_gamma 2.2\n',
            '    max_trace_level 5\n',
            '}\n',
            '\n',
            '// -----------------------------------------------------------\n',
            '\n',
            '#macro rotate_view_for_animation()\n',
            '    // If using the [filename.pov].ini file, with animation enabled, this will produce\n',
            '    // a cyclic animation of the scene rotating, otherwise this will not affect the image:\n',
            '    rotate <0,clock*360,0>\n',
            '#end\n',
            '\n',
            '#macro ccdc_perspective_camera( camera_position, field_of_view )\n',
            '    camera {\n',
            '        perspective\n',
            '        location camera_position\n',
            '        up    <0,1,0>\n',
            '        right  -x * (image_width/image_height)\n',
            '        look_at <0,0,-100>\n',
            '        // Convert the vertical field of view to the horizontal field of view\n',
            '        angle degrees(2 * atan2(tan(radians(field_of_view / 2)) * image_width, image_height))\n',
            '\n',
            '        rotate_view_for_animation()\n',
            '    }\n',
            '#end\n',
            '\n',
            '#macro ccdc_directional_light_source( light_position, light_diffuse_colour, light_specular_colour )\n',
            '    // The scalar multiplier applied to light_position seems to be needed for correct brightness\n',
            '    light_source {\n',
            '        5 * light_position\n',
            '        light_diffuse_colour\n',
            '        parallel\n',
            '        shadowless\n',
            '        rotate_view_for_animation()\n',
            '    }\n',
            '    light_source {\n',
            '        5 * light_position\n',
            '        light_specular_colour\n',
            '        parallel\n',
            '        rotate_view_for_animation()\n',
            '    }\n',
            '#end\n',
            '\n',
            '#macro ccdc_ambient_light_source( light_colour )\n',
            '    global_settings { ambient_light light_colour * 10 }\n',
            '#end\n',
            '\n',
            '#macro ccdc_background_colour( background_colour )\n',
            '    background { background_colour }\n',
            '#end\n',
            '\n',
            '\n',
            '#macro ccdc_orient_world( world_orientation )\n',
            '    transform { world_orientation }\n',
            '#end\n',
            '\n',
            '#macro ccdc_orient_structure( structure_orientation )\n',
            '    transform { structure_orientation }\n',
            '#end\n',
            '\n',
            '#macro ccdc_set_standard_mercury_solid_material_properties( object_color )\n',
            '    no_shadow\n',
            '    texture {\n',
            '        pigment { object_color }\n',
            '        finish {\n',
            '            specular 0.2\n',
            '            roughness 0.02\n',
            '        }\n',
            '    }\n',
            '#end\n',
            '\n',
            '#macro ccdc_set_shiny_solid_material_properties( object_color )\n',
            '    no_shadow\n',
            '    texture {\n',
            '        pigment { object_color }\n',
            '        finish {\n',
            '            specular 0.8\n',
            '            roughness 0.02\n',
            '        }\n',
            '    }\n',
            '#end\n',
            '\n',
            '#macro ccdc_set_matt_solid_material_properties( object_color )\n',
            '    no_shadow\n',
            '    texture {\n',
            '        pigment { object_color }\n',
            '        finish {\n',
            '            specular 0.0\n',
            '            roughness 0.02\n',
            '        }\n',
            '    }\n',
            '#end\n',
            '\n',
            '#macro ccdc_set_wireframe_material_properties( object_color )\n',
            '    no_shadow\n',
            '    pigment { object_color }\n',
            '#end\n',
            '\n',
            '\n',
            '#macro ccdc_draw_solid_sphere( position, sphere_radius, sphere_color )\n',
            '    sphere {\n',
            '        position, sphere_radius\n',
            '        ccdc_set_matt_solid_material_properties( sphere_color )\n',
            '    }\n',
            '#end\n',
            '\n',
            '\n',
            '#macro ccdc_draw_stippled_line_segment( line_begin, line_end, radio,step, line_color )\n',
            '    // TODO - adjust to use stipple and stipple_scale_factor\n',
            '    /* For example:\n',
            '\n',
            '        AACRUB delocalised bonds:\n',
            '        61680 = F0F0\n',
            '        \n',
            '        AABHTZ contacts:\n',
            '        43690 = AAAA\n',
            '    */\n',
            '    // The following is approximately correct when drawing contacts\n',
            '    #declare nsteps = step;\n',
            '    #declare increment = 1 / nsteps;\n',
            '    #declare scalar1 = 0.0;\n',
            '    #while ( scalar1 < 1.0 )\n',
            '        #declare point1 = ( scalar1 * line_begin ) + ( 1 - scalar1 ) * line_end;\n',
            '        #declare scalar2 = scalar1 + ( increment / 2.0 );\n',
            '        #declare point2 = ( scalar2 * line_begin ) + ( 1 - scalar2 ) * line_end;\n',
            '        cylinder {\n',
            '            point1, point2, radio\n',
            '            ccdc_set_wireframe_material_properties( line_color )\n',
            '        }\n',
            '        #declare scalar1 = scalar1 + increment;\n',
            '    #end\n',
            '#end\n',
            '\n',
            '\n',
            '\n',
            '\n',
            '#macro ccdc_draw_closed_cylinder( centre_line_begin, centre_line_end, cylinder_radius, cylinder_color )\n',
            '    cylinder {\n',
            '        centre_line_begin, centre_line_end, cylinder_radius\n',
            '        ccdc_set_matt_solid_material_properties( cylinder_color )\n',
            '    }\n',
            '#end\n',
            '\n',
            '\n',
            '\n',
            '\n',
            '\n',
            '\n',
            '// -----------------------------------------------------------\n',
            '\n',
            '// You can edit the file "ccdc_macro_overrides.inc" in this directory\n',
            '// to override the implementations of any or all the above POVRay macros:\n',
            '//#include "ccdc_macro_overrides.inc"\n',
            '\n',
            '#declare font_scale = 0.163381;\n',
            '\n',
            '#declare font_name = "cyrvetic.ttf";\n',
            '\n',
            'ccdc_perspective_camera( < 0, 0, ' + p + ' >, 0.05 )\n',
            'ccdc_directional_light_source( < 1, 1, 1 >, rgb < 0.701961, 0.701961, 0.701961 >, rgb < 1, 1, 1 > )\n',
            'ccdc_directional_light_source( < -1, 0.2, 1 >, rgb < 0.501961, 0.501961, 0.501961 >, rgb < 0.501961, 0.501961, 0.501961 > )\n',
            'ccdc_ambient_light_source( rgb < 0.301961, 0.301961, 0.301961 > )\n',
            'ccdc_background_colour( rgb < 1, 1, 1 > )\n',
            'union {\n',
            '    union {\n',
        ]

        #        // atom C
        #        ccdc_draw_solid_sphere( < 0.283, 0.317, 0.138 >, 0.425, rgb < 0.466667, 0.466667, 0.466667 > )

        #        // 00000001 bonds
        #        // bond C-C
        #        ccdc_draw_closed_cylinder( < 0.283, 0.317, 0.138 >, < 1.353, 1.153, -0.223 >, 0.1, rgb < 0.466667, 0.466667, 0.466667 > )

        #        // bond C-H
        #        ccdc_draw_stippled_line_segment( < -2.148, 0.139, 0.913 >, < -2.414, -0.2565, 0.468 >, 13107, 1, rgb < 0.466667, 0.466667, 0.466667 > )

        tail_txt = [
            '    }\n',
            '}\n'
        ]
        return head_txt, tail_txt

    def run_Extract(self,files):
        for file in files:
            title = file.split('.')[0]
            self.atom[title] = []
            self.coord[title] = []
            self.bond[title] = []
            input_file = open(file, 'r')
            line = input_file.readline()
            while len(line.split()) != 2 or not line.split()[0].isdigit() or not line.split()[0].isdigit():
                line = input_file.readline()
            line = input_file.readline()
            while len(''.join(line.split())) != 0:
                self.atom[title].append(line.split()[0])
                self.coord[title].append(",".join(line.split()[1:4]))
                line = input_file.readline()
            line = input_file.readline()
            while len(''.join(line.split())) != 0:
                if len(''.join(line.split())) == 1:
                    line = input_file.readline()
                else:
                    for n in range(1, len(line.split())):
                        if n % 2 != 0:
                            self.bond[title].append([line.split()[0], line.split()[n]])
                        else:
                            self.bond[title][-1].append(line.split()[n])
                    line = input_file.readline()

    def run_Atom(self,files):
        atom_txt = []
        for file in files:
            title = file.split('.')[0]
            for n in range(len(self.atom[title])):
                atom_txt.append( "       // atom  {} \n".format(self.atom[title][n]))
                atom_txt.append("        ccdc_draw_solid_sphere( < {} >, {}, rgb < {} >  )\n\n".format(self.coord[title][n],self.raio_atom[self.atom[title][n]],self.cor_atom[self.atom[title][n]]))
        return atom_txt

    def run_Bond(self,files):
        bond_txt = []
        for file in files:
            title = file.split('.')[0]
            for n in range(len(self.bond[title])):
                if self.bond[title][n][2] == '0.5':
                    bond_txt.append("       // ts_bond  {} {}\n".format(self.atom[title][int(self.bond[title][n][0])-1],self.atom[title][int(self.bond[title][n][1])-1]))
                    bond_txt.append("        ccdc_draw_stippled_line_segment( < {} >,< {} >, {}, {}, rgb < {}>  )\n\n".format(self.coord[title][int(self.bond[title][n][0])-1], self.coord[title][int(self.bond[title][n][1])-1],  self.raio_bond_ts,self.step_ts, self.cor_bond_ts))
                else:
                    bond_txt.append("       // bond  {} {}\n".format(self.atom[title][int(self.bond[title][n][0])-1],self.atom[title][int(self.bond[title][n][1])-1]))
                    bond_txt.append("        ccdc_draw_closed_cylinder( < {} >,< {} >, {}, rgb < {} > )\n\n".format(self.coord[title][int(self.bond[title][n][0])-1],self.coord[title][int(self.bond[title][n][1])-1],self.raio_bond,self.cor_bond))

                if self.bond[title][n][2] == '2.0' and False:
                    coord1 = ','.join([str(x) for x in [np.array([float(x) for x in self.coord[title][int(self.bond[title][n][0]) - 1].split(',')]) + np.array([0.05, 0.05, 0.05])]])
                    coord2 = ','.join([str(x) for x in [np.array([float(x) for x in self.coord[title][int(self.bond[title][n][1]) - 1].split(',')]) + np.array([0.05, 0.05, 0.05])]])
                    coord3 = ','.join([str(x) for x in [np.array([float(x) for x in self.coord[title][int(self.bond[title][n][0]) - 1].split(',')]) - np.array([0.05, 0.05, 0.05])]])
                    coord4 = ','.join([str(x) for x in [np.array([float(x) for x in self.coord[title][int(self.bond[title][n][1]) - 1].split(',')]) - np.array([0.05, 0.05, 0.05])]])

                    bond_txt.append("       // bond  {} {}\n".format(self.atom[title][int(self.bond[title][n][0])-1],self.atom[title][int(self.bond[title][n][1])-1]))
                    bond_txt.append("        ccdc_draw_closed_cylinder( < {} >,< {} >, {}, rgb < {} > )\n\n".format(coord1[1:-2],coord2[1:-2],self.raio_bond,self.cor_bond))
                    bond_txt.append("        ccdc_draw_closed_cylinder( < {} >,< {} >, {}, rgb < {} > )\n\n".format(coord3[1:-2],coord4[1:-2],self.raio_bond,self.cor_bond))

        return bond_txt



    def run(self,persp = 1,files = 'none',files_out = 'none'):
        if files == 'none':
            files = [x for x in os.listdir() if '.gjf' in x]
        self.run_Extract(files)
        atom_txt = self.run_Atom(files)
        bond_txt = self.run_Bond(files)

        if files_out == 'none':
            files_out = [x.split('.')[0]+'.pov' for x in files]

        head_txt, tail_txt = self.Text(persp)

        for file in files_out:
            out = open(file,'w')
            out.writelines(head_txt)
            out.writelines(atom_txt)
            out.writelines(bond_txt)
            out.writelines(tail_txt)
            out.close()



