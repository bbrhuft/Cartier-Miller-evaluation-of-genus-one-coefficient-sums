// Quarter-prefix adapter, GPL-2.0-or-later; uses unchanged Sage/Harvey sources.
#include <NTL/ZZ_pX.h>
#include <NTL/lzz_pX.h>
#include <NTL/mat_ZZ_p.h>
#include <NTL/version.h>
#include <NTL/BasicThreadPool.h>
#include "upstream/hypellfrob.h"
#include "upstream/recurrences_ntl.h"
#include <chrono>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace NTL;
using Clock = std::chrono::steady_clock;
struct Result {
    ZZ B,a,U,A,C,D;
    double setup_ms,kernel_ms,finish_ms,total_ms;
};
Result calculate(const ZZ& p, const ZZ& L, bool force_big) {
    auto t0=Clock::now();
    ZZ_p::init(p);
    mat_ZZ_p M0,M1;
    M0.SetDims(2,2); M1.SetDims(2,2);
    M0[0][0]=-1;
    M1[0][0]=2; M1[0][1]=4; M1[1][1]=4;
    std::vector<ZZ> target{ZZ(0),L};
    mat_ZZ_p P;
    auto t1=Clock::now();
    if(IsZero(L)) ident(P,2);
    else if(force_big) {
        std::vector<mat_ZZ_p> out;
        hypellfrob::ntl_interval_products<ZZ_p,ZZ_pX,ZZ_pXModulus,
           vec_ZZ_p,mat_ZZ_p,FFTRep>(out,M0,M1,target);
        P=out.at(0);
    } else hypellfrob::hypellfrob_interval_products_wrapper(P,M0,M1,target);
    auto t2=Clock::now();
    if(!IsZero(P[1][0]) || IsZero(P[1][1]))
        throw std::runtime_error("invalid triangular product or zero denominator");
    ZZ_p di=inv(P[1][1]);
    ZZ_p a=P[0][0]*di, B=P[0][1]*di;
    ZZ_p l=conv<ZZ_p>(L);
    ZZ_p U=4*B-2*l*(2*l+5)*a;
    auto t3=Clock::now();
    auto ms=[](Clock::time_point x,Clock::time_point y){
        return std::chrono::duration<double,std::milli>(y-x).count();
    };
    return {rep(B),rep(a),rep(U),rep(P[0][0]),rep(P[0][1]),rep(P[1][1]),
       ms(t0,t1),ms(t1,t2),ms(t2,t3),ms(t0,t3)};
}
int main(int argc,char** argv) {
    SetNumThreads(1);
    if(argc==2 && std::string(argv[1])=="--version") {
        std::cout<<"{\"ntl\":\""<<NTL_VERSION
          <<"\",\"compiler\":\""<<__VERSION__<<"\",\"ntl_threads\":1}\n";return 0;
    }
    bool force_big=argc==2 && std::string(argv[1])=="--force-big";
    if(argc>1 && !force_big) {std::cerr<<"usage: harvey_adapter [--force-big|--version]\n";return 2;}
    std::string line;
    while(std::getline(std::cin,line)) {
      if(line.empty())continue;
      try {
        std::istringstream in(line);ZZ p,L;int reps;
        if(!(in>>p>>L>>reps)||p<7||L<0||2*L>p-1||reps<1||reps>10000)
          throw std::runtime_error("expected prime p>=7, 0<=L<=(p-1)/2, repetitions 1..10000");
        if(!ProbPrime(p,30))throw std::runtime_error("input modulus is not prime");
        std::vector<Result> rows;
        for(int i=0;i<reps;i++)rows.push_back(calculate(p,L,force_big));
        const auto& r=rows.back();
        std::cout.precision(12);
        std::cout<<"{\"p\":"<<p<<",\"L\":"<<L
          <<",\"B\":"<<r.B<<",\"a\":"<<r.a<<",\"U\":"<<r.U
          <<",\"A\":"<<r.A<<",\"C\":"<<r.C<<",\"D\":"<<r.D
          <<",\"backend\":\""<<(force_big?"ZZ_p_forced":(p.SinglePrecision()?"zz_p_auto":"ZZ_p_auto"))
          <<"\",\"samples\":[";
        for(int i=0;i<reps;i++) {
          if(i)std::cout<<",";
          const auto& s=rows[i];
          if(s.a!=r.a||s.B!=r.B||s.U!=r.U)throw std::runtime_error("repeat mismatch");
          std::cout<<"{\"setup_ms\":"<<s.setup_ms<<",\"kernel_ms\":"<<s.kernel_ms
           <<",\"finish_ms\":"<<s.finish_ms<<",\"total_ms\":"<<s.total_ms<<"}";
        }
        std::cout<<"]}"<<std::endl;
      }catch(const std::exception& e){std::cerr<<e.what()<<std::endl;return 1;}
    }
}
