#include <iostream>
#include <algorithm>
#include <gmpxx.h>
#include <vector>

#include "fp.h"

using namespace std;

int GetGeneratorN()
{
    size_t N = 200;

    mpz_class P1{"536903680",10};
    mpz_class rexp{"524320",10};

    vector<mpz_class> subgroups;
    subgroups.push_back(mpz_class(32));
    subgroups.push_back(mpz_class(5));
    subgroups.push_back(mpz_class(23));
    subgroups.push_back(mpz_class(119));

    FP f1(mpz_class(1));
    FP g(mpz_class(1));
    FP h(mpz_class(1));
    FP l(mpz_class(1));

    for(size_t i=2;i<N;++i){
        g.set(mpz_class(static_cast<int>(i)));
        h = g^P1;
        if(h==f1){
            cout << "Got one! g = ";
            cout << g.val() << ", h = " << h.val() << ", Subgroup orders: ";
            l = g^rexp;
            for(auto v:subgroups){
                h = l^v;
                cout << h.val() << ", ";
                if(h==f1){
                    cout << "(We are doomed!), ";
                }
            }
            cout << endl;
        }
    }

    return 0;
}

int GetGenerator2N()
{
    size_t N = 200;

    mpz_class P1{"536903680",10};
    mpz_class rexp{"262160",10};

    vector<mpz_class> subgroups;
    subgroups.push_back(mpz_class(16));
    subgroups.push_back(mpz_class(5));
    subgroups.push_back(mpz_class(23));
    subgroups.push_back(mpz_class(119));

    FP f1(mpz_class(1));
    FP g(mpz_class(1));
    FP h(mpz_class(1));
    FP l(mpz_class(1));

    for(size_t i=2;i<N;++i){
        g.set(mpz_class(static_cast<int>(i)));
        h = g^P1;
        if(h==f1){
            cout << "Got one! g = ";
            cout << g.val() << ", h = " << h.val() << ", Subgroup orders: ";
            l = g^rexp;
            for(auto v:subgroups){
                h = l^v;
                cout << h.val() << ", ";
                if(h==f1){
                    cout << "(We are doomed!), ";
                }
            }
            cout << endl;
        }
    }

    return 0;
}

int GenerateNthRootSet(FP *gp)
{
    FP g(mpz_class(3));//group generator
    FP fp1(mpz_class(1));//Unit element

    FP omega;
    omega = g^mpz_class(524320); //primitive n'th root of unity or simply omega

    mpz_class exp(0);
    mpz_class gp_order(1024);

    for(int i=0;i<1024;++i){
        exp = i;
        gp[i] = (omega^i);
    }

//    for(int i=0;i<1024;++i){
//        r = gp[i]^gp_order;
//        if(r!=fp1){
//            cout << r.val() << " Sob gondogol!" << endl;
//        }
//    }
    return 0;
}

int Generate2NthRootSet(FP *gp)
{
    FP g(mpz_class(3));//group generator
    FP fp1(mpz_class(1));//Unit element

    FP omega;
    omega = g^mpz_class(524320); //primitive n'th root of unity or simply omega

    FP phi;
    phi = g^mpz_class(262160); //primitive 2n'th root of unity or simply phi

    mpz_class exp(0);
    mpz_class gp_order(2048);

    //Need n=1024 values, make 2048 to get negative solutions
    for(int i=0;i<1024;++i){
        exp = i;
        gp[i] = (phi^i);
    }

//    for(int i=0;i<1024;++i){
//        r = gp[i]^gp_order;
//        if(r!=fp1){
//            cout << r.val() << " Sob gondogol!" << endl;
//        }
//    }

//    for(int i=0;i<1024;++i){
//        r = gp[i]^2;
//        if(r==omega){
//            cout << gp[i].val() << ", " << omega.val() << ", Peyechi!" << endl;
//        }
//    }

    return 0;
}

int GenerateOmegaComplements(FP *omega_n_set)
{
    FP g(mpz_class(3));//group generator
    FP omega_inv;

    FP omega;
    omega = g^mpz_class(524320); //primitive n'th root of unity or simply omega
    omega_inv = ~omega;

    mpz_class exp(0);

    for(int i=0;i<1024;++i){
        exp = i;
        omega_n_set[i] = (omega_inv^i);
    }

    return 0;
}

int GeneratePhiComplements(FP *phi_n_set)
{
    FP g(mpz_class(3));//group generator
    FP phi;
    FP phi_n;
    phi = g^mpz_class(262160); //primitive 2n'th root of unity or simply phi
    phi_n = ~phi;

    for(int i=0;i<1024;++i){
        phi_n_set[i] = phi_n ^ i;
    }

    return 0;
}

int GenerateReverseBitOrder(unsigned int *r_idx = nullptr)
{
    unsigned int rev = 0;
    unsigned int n = 0;

    for(unsigned int i=0;i<1024;++i){
        n = i;
        rev = 0;
        for(int j=0;j<10;++j)
        {
            rev <<= 1;
            if((n & 1) == 1){
                rev ^= 1;
            }
            n >>= 1;
        }
        r_idx[i] = rev;
    }
    return 0;
}

int NTT(FP *C, FP *A, FP *omega_set)
{
    //O(NlogN)
    int pidx = 0;

    FP T[1024];
    unsigned int RIDX_LUT[1024];

    GenerateReverseBitOrder(RIDX_LUT);

    for(int i=0;i<1024;++i){
        T[i] = A[RIDX_LUT[i]];
    }

    for(int i=0;i<10;++i){
        for(int j=0;j<512;++j){
            pidx = (j >> (9-i)) << (9-i);
            C[j] = T[j << 1] + (T[(j << 1) + 1] * omega_set[pidx]);
            C[j+512] = T[j << 1] - (T[(j << 1) + 1] * omega_set[pidx]);
        }

        for(int i=0;i<1024;++i){
            T[i] = C[i];
        }
    }

    for(int i=0;i<1024;++i){
        C[i] = T[i];
    }

    return 0;
}

int INTT(FP *C, FP *A, FP *omega_set)
{
    //O(NlogN)
    int pidx = 0;

    FP Nn(mpz_class(1024));
    FP Ninv;

    Ninv = ~Nn;

    FP T[1024];
    unsigned int RIDX_LUT[1024];

    GenerateReverseBitOrder(RIDX_LUT);

    for(int i=0;i<1024;++i){
        T[i] = A[RIDX_LUT[i]];
    }

    for(int i=0;i<10;++i){
        for(int j=0;j<512;++j){
            pidx = (j >> (9-i)) << (9-i);
            C[j] = T[j << 1] + (T[(j << 1) + 1] * omega_set[pidx]);
            C[j+512] = T[j << 1] - (T[(j << 1) + 1] * omega_set[pidx]);
        }

        for(int i=0;i<1024;++i){
            T[i] = C[i];
        }
    }

    for(int i=0;i<1024;++i){
        C[i] = T[i] * Ninv;
    }

    return 0;
}

int PolyNTT()
{
    mpz_class f0(0);

    FP *omega_set;
    FP *omega_n_set;
    FP *phi_set;
    FP *phi_n_set;

    FP *A;
    FP *B;

    FP *A_bar;
    FP *B_bar;

    FP *AA;
    FP *BB;

    FP *C;
    FP *CC;
    FP *C_bar;

    omega_set = new FP[1024];
    omega_n_set = new FP[1024];

    phi_set = new FP[1024];
    phi_n_set = new FP[1024];

    A = new FP[1024];
    B = new FP[1024];

    A_bar = new FP[1024];
    B_bar = new FP[1024];

    AA = new FP[1024];
    BB = new FP[1024];

    C = new FP[1024];
    CC = new FP[1024];
    C_bar = new FP[1024];

    for(int i=0;i<1024;++i){
        A[i].set(f0);
        B[i].set(f0);

        A_bar[i].set(f0);
        B_bar[i].set(f0);

        AA[i].set(f0);
        BB[i].set(f0);

        C[i].set(f0);
        CC[i].set(f0);
        C_bar[i].set(f0);
    }

    A[1].set(mpz_class(5));
    A[2].set(mpz_class(10));
    A[3].set(mpz_class(20));

    B[1].set(mpz_class(2));
    B[2].set(mpz_class(3));
    B[3].set(mpz_class(5));

//    GetGeneratorN();
    GenerateNthRootSet(omega_set);
    Generate2NthRootSet(phi_set);
    GenerateOmegaComplements(omega_n_set);
    GeneratePhiComplements(phi_n_set);

    for(int i=0;i<1024;++i){
        A_bar[i] = A[i] * phi_set[i];
        B_bar[i] = B[i] * phi_set[i];
    }

    NTT(AA,A_bar,omega_set);
    NTT(BB,B_bar,omega_set);

    for(int i=0;i<1024;++i){
        CC[i] = AA[i] * BB[i];
    }

    INTT(C_bar,CC,omega_n_set);

    for(int i=0;i<1024;++i){
        C[i] = C_bar[i] * phi_n_set[i];
    }

    //Print input and output values

    for(int i=0;i<16;++i){
        cout << A[i].val() << " ";
    }

    cout << endl;

    for(int i=0;i<16;++i){
        cout << B[i].val() << " ";
    }

    cout << endl;

    for(int i=0;i<16;++i){
        cout << C[i].val() << " ";
    }

    cout << endl;

    delete [] omega_set;
    delete [] omega_n_set;

    delete [] phi_set;
    delete [] phi_n_set;

    delete [] A;
    delete [] B;

    delete [] A_bar;
    delete [] B_bar;

    delete [] AA;
    delete [] BB;

    delete [] C;
    delete [] CC;
    delete [] C_bar;
    return 0;
}

int main()
{
    cout << "Precuations!" << endl;
    cout << "None of the functions allocats memory for input arrays or output arrays.\nThese all need to be allocated before passing to the function." << endl;

    PolyNTT();

    return 0;
}
