#ifndef FP_H
#define FP_H

#include <gmp.h>
#include <gmpxx.h>
#include <iostream>

class FP
{

static mpz_class P;
mpz_class x;

public:
    FP();
    FP(mpz_class x);
    ~FP();

    FP operator=(FP v);
    FP operator+(FP v);
    FP operator-(FP v);
    FP operator!();
    FP operator*(FP v);
    FP operator^(mpz_class mexp);
    FP operator~();
    bool operator==(FP v);
    bool operator!=(FP v);
    mpz_class val();
    int set(mpz_class v);
};

#endif // FP_H
