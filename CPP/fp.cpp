#include "fp.h"

mpz_class FP::P = mpz_class{"536903681",10};

FP::FP()
{
    this->x.set_str("0",10);
}

FP::FP(mpz_class x)
{
    mpz_mod(this->x.get_mpz_t(),x.get_mpz_t(),this->P.get_mpz_t());
}

FP::~FP()
{
    this->x.set_str("0",10);
}

FP FP::operator=(FP v)
{
    this->x = v.x;
    return v;
}

FP FP::operator+(FP v)
{
    FP t;
    t.x = this->x + v.x;
    mpz_mod(t.x.get_mpz_t(),t.x.get_mpz_t(),this->P.get_mpz_t());
    return t;
}

FP FP::operator-(FP v)
{
    FP t;
    t.x = this->x - v.x;
    mpz_mod(t.x.get_mpz_t(),t.x.get_mpz_t(),this->P.get_mpz_t());
    return t;
}

FP FP::operator!()
{
    FP t;
    t.x = mpz_class("0",10) - this->x;
    mpz_mod(t.x.get_mpz_t(),t.x.get_mpz_t(),this->P.get_mpz_t());
    return t;
}

FP FP::operator*(FP v)
{
    FP t;
    t.x = this->x * v.x;
    mpz_mod(t.x.get_mpz_t(),t.x.get_mpz_t(),this->P.get_mpz_t());
    return t;
}

FP FP::operator^(mpz_class mexp)
{
    FP t;
    mpz_powm(t.x.get_mpz_t(),this->x.get_mpz_t(),mexp.get_mpz_t(),this->P.get_mpz_t());
    return t;
}

FP FP::operator~()
{
    FP t;
    mpz_class iexp = this->P-2;
    mpz_powm(t.x.get_mpz_t(),this->x.get_mpz_t(),iexp.get_mpz_t(),this->P.get_mpz_t());
    return t;
}

bool FP::operator==(FP v)
{
    return this->x == v.x;
}

bool FP::operator!=(FP v)
{
    return this->x != v.x;
}

mpz_class FP::val()
{
    return this->x;
}

int FP::set(mpz_class v)
{
    this->x = v;
    return 0;
}
