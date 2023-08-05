# *
# * Authors:     Scipion Team
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion-users@lists.sourceforge.net'
# *
# **************************************************************************

from pwem.emlib.image import ImageHandler
import pyworkflow.utils as pwutils
from relion.convert.convert_base import WriterBase
from scipion.install.funcs import mkdir
import numpy as np
import relion
from os.path import abspath, join
from pwem.convert.transformations import translation_from_matrix, euler_from_matrix
from relion.convert import Table


class Writer(WriterBase):
    """ Helper class to convert from Scipion SetOfImages subclasses
    with star file format previous to Relion>3.1, but providing the same
     interface as the new Writer class.
    """

    def writeSetOfSubtomograms(self, subtomoSet, subtomosStar, **kwargs):
        currentTomo = ''
        MRC = 'mrc'
        ih = ImageHandler()
        tomoTable = self._createStarTomoTable()
        tmpDir = pwutils.getParentFolder(subtomosStar)
        for subtomo in subtomoSet:
            if pwutils.getExt(subtomo.getFileName()) != '.' + MRC:
                mrcDir = join(tmpDir, pwutils.removeBaseExt(subtomo.getVolName()))
                if currentTomo != subtomo.getVolName():
                    mkdir(mrcDir)
                mrcFile = join(mrcDir, pwutils.replaceBaseExt(subtomo.getFileName(), MRC))
                ih.convert(subtomo.getFileName(), mrcFile)
            angles, shifts = self._getTransformInfoFromSubtomo(subtomo)
            magn = subtomo.getAcquisition().getMagnification()
            rlnMicrographName = subtomo.getVolName()
            rlnCoordinateX = subtomo.getCoordinate3D().getX()
            rlnCoordinateY = subtomo.getCoordinate3D().getY()
            rlnCoordinateZ = subtomo.getCoordinate3D().getZ()
            rlnImageName = subtomo.getFileName()
            rlnCtfImage = abspath(self._getCTFFileFromSubtomo(subtomo))
            rlnMagnification = magn if magn else 10000 #64000
            rlnDetectorPixelSize = subtomo.getSamplingRate()
            rlnAngleRot = angles[0]
            rlnAngleTilt = angles[1]
            rlnAnglePsi = angles[2]
            rlnOriginX = shifts[0]
            rlnOriginY = shifts[1]
            rlnOriginZ = shifts[2]
            # Add row to the table which will be used to generate the STAR file
            tomoTable.addRow(rlnMicrographName,
                             rlnCoordinateX,
                             rlnCoordinateY,
                             rlnCoordinateZ,
                             rlnImageName,
                             rlnCtfImage,
                             rlnMagnification,
                             rlnDetectorPixelSize,
                             rlnAngleRot,
                             rlnAngleTilt,
                             rlnAnglePsi,
                             rlnOriginX,
                             rlnOriginY,
                             rlnOriginZ
                             )
        # Write the STAR file
        if relion.Plugin.IS_30():
            tomoTable.write(subtomosStar)
        # else:
        #     tmpTable = self._getTmpPath('tbl.star')
        #     tomoTable.write(tmpTable)
        #     # Re-write the star file as expected by the current version of Relion, if necessary
        #     starFile = abspath(subtomosStar)
        #     self.runJob('relion_convert_star',
        #                 ' --i %s --o %s' % (tmpTable, starFile))

    @ staticmethod
    def _createStarTomoTable():
        return Table(columns=['rlnMicrographName',
                              'rlnCoordinateX',
                              'rlnCoordinateY',
                              'rlnCoordinateZ',
                              'rlnImageName',
                              'rlnCtfImage',
                              'rlnMagnification',
                              'rlnDetectorPixelSize',
                              'rlnAngleRot',
                              'rlnAngleTilt',
                              'rlnAnglePsi',
                              'rlnOriginX',
                              'rlnOriginY',
                              'rlnOriginZ',
                              ])

    @ staticmethod
    def _getCTFFileFromSubtomo(subtomo):
        try:
            return subtomo.getCoordinate3D()._3dcftMrcFile.get()
        except:
            return 'Unavailable'

    @staticmethod
    def _getTransformInfoFromSubtomo(subtomo, calcInv=True):
        angles = [0, 0, 0]
        shifts = [0, 0, 0]
        T = subtomo.getTransform()

        if T:  # Alignment performed before
            M = subtomo.getTransform().getMatrix()
            shifts = translation_from_matrix(M)
            if calcInv:
                shifts = -shifts
                M = np.linalg.inv(M)

            angles = -np.rad2deg(euler_from_matrix(M, axes='szyz'))

        return angles, shifts
