import  numpy       as np

class GLON( object ):

    def GLON( self, nitem, auxcode='' ):

        bounds  = (0, 360)

        offset  = abs( (bounds[0] - bounds[1]) / 2. / nitem ) if 'M' in auxcode   \
             else 0

        coords  = np.linspace( bounds[0]+offset, bounds[1]-offset, nitem )

        if 'I' in auxcode:
            return coords[::-1]

        else:
            return coords
