#include <stdlib.h>

// declare callback function type
typedef void _callback_func(int step, int dim1, int dim2, double* ppArray, void* pObj);

// process method to multiply vertex-coordinates with scale value in each step
int process(int num_steps, double scale, int dim1, int dim2, double** verts, _callback_func cb_func, void* pObj) {

    if (verts == NULL) {
        return -1;
    }

    // Allocate buffer
    double* pBuff = (double*)malloc(sizeof(double) * dim1 * dim2);

    //  set initial value to the buffer
    for (int i = 0; i < dim1; i++) {
        for (int j = 0; j < dim2; j++) {
            pBuff[i*dim2 + j] = verts[i][j];
        }
    }

    for (int s = 0; s < num_steps; s++) {

        // multiply element values in each step
        for (int i = 0; i < dim1; i++) {
            for (int j = 0; j < dim2; j++) {
                pBuff[i*dim2 + j] *= scale;
            }
        }

        // call the callback function to pass the parameters
        if (cb_func != NULL) {
            cb_func(s, dim1, dim2, pBuff, pObj);
        }
    }

    // Release buffer
    free(pBuff);

    return 0;
}

