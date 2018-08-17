import  numpy       as np

class NUMBER( object ):

    def NUMBER( self, nitem, auxcode='' ):

        bounds  = (0, nitem-1)

        offset  = abs( (bounds[0] - bounds[1]) / 2. / nitem ) if 'M' in auxcode   \
             else 0

        coords  = np.linspace( bounds[0]+offset, bounds[1]-offset, nitem )

        if 'I' in auxcode:
            return coords[::-1]

        else:
            return coords
