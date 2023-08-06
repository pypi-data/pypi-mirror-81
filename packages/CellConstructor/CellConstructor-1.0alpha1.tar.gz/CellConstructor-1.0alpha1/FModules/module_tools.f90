module tools

use polarization
use stochastic

public :: trace
public :: fourtotwo 
public :: fourtotwo_real !LM added
public :: twotofour 
public :: generate_hermitian_basis 
public :: generate_hermitian_basis_2 
public :: gram_schmidt_mat
public :: gram_schmidt_pol_vect
public :: dotprodmat
public :: project_dyn
public :: coefftwotone
public :: coeffonetotwo
public :: generate_translation_generator
public :: generate_displacement_basis
public :: project_generators_onto_translations
public :: is_nan !LM added

contains

! This subroutine checks if the effective charges with different q's 
! give different phonon frequencies. If all frequencies are the same
! then single_q = .true., else single_q = .false.

subroutine set_single_q (nat,itau,epsil,zeu,omega,ityp,amass,single_q)

  implicit none

  integer, intent(in) :: nat
  integer, dimension(:), intent(in) :: itau
  double precision, dimension(3,3), intent(in) :: epsil    
  double precision, dimension(:,:,:), intent(in) :: zeu
  double precision, intent(in) :: omega
  integer, dimension(:), intent(in) :: ityp
  double precision, dimension(:), intent(in) :: amass
  logical, intent(out) :: single_q

  integer :: i
  double precision, dimension(3) :: q_eff_charge
  double precision, dimension(:), allocatable :: w1, w2
  double complex, dimension(:,:,:), allocatable :: e
  double complex, dimension(:,:,:,:), allocatable :: phi_nonanal
  double precision :: rydcm1

  rydcm1 = 13.6058d0*8065.5d0

  ! Allocate variables

  allocate(w1(3*nat))
  allocate(w2(3*nat))
  allocate(e(3*nat,nat,3))
  allocate(phi_nonanal(3,3,nat,nat))

  ! Assign a random q vector

  call random_sphere(q_eff_charge)
  
  print '(a,3f12.6)', '  random q = ', q_eff_charge(:) 

  phi_nonanal = (0.0d0,0.0d0)

  ! Create the nonanalytica part of the dynamical matrix and diagonalize

  call nonanal ( nat, nat, itau, epsil, q_eff_charge, zeu, omega, phi_nonanal )
  call dyndiag ( nat, phi_nonanal, ityp, amass, w1, e)

  print *, ' Frequencies :'

  do i = 1, 3*nat
    print '(a,i5,a,f12.8,a)', '    w ', i, ' = ', w1(i)*rydcm1, ' [cm-1] '        
  end do

  ! Assign a new random q vector

  call random_sphere(q_eff_charge(:))

  print '(a,3f12.6)', '  random q = ', q_eff_charge(:) 

  phi_nonanal = (0.0d0,0.0d0)

  ! Create the nonanalytica part of the dynamical matrix and diagonalize

  call nonanal ( nat, nat, itau, epsil, q_eff_charge, zeu, omega, phi_nonanal )
  call dyndiag ( nat, phi_nonanal, ityp, amass, w2, e)  

  print *, ' Frequencies :'

  do i = 1, 3*nat
    print '(a,i5,a,f12.8,a)', '    w ', i, ' = ', w2(i)*rydcm1, ' [cm-1] '        
  end do

  ! Check if frequencies are equal or not in the two calculations

  single_q = .true.  

  do i = 1, 3*nat
    if ( abs(w1(i) - w2(i))*rydcm1 .gt. 0.1d0 ) single_q = .false.
  end do

  ! Deallocate stuff

  deallocate(w1,w2,e,phi_nonanal)

end subroutine set_single_q

! This subroutine projects some generators onto the translations 
! space

subroutine project_generators_onto_translations ( n, gt, gh)

  implicit none

  integer, intent(in) :: n
  double complex, dimension(:,:,:,:,:), intent(in) :: gt
  double complex, dimension(:,:,:,:,:), intent(inout) :: gh

  integer :: i, alpha, j
  integer :: nat
  double complex, dimension(:,:,:,:), allocatable :: iden, proj
  double complex, dimension(:,:), allocatable :: gh2, proj2, gh_aux

  nat = size(gt(1,1,1,:,1))

  allocate(iden(3,3,nat,nat))
  allocate(proj(3,3,nat,nat))
  allocate(gh2(3*nat,3*nat))
  allocate(proj2(3*nat,3*nat))
  allocate(gh_aux(3*nat,3*nat))

  iden = (0.0d0,0.0d0)

  do i = 1, nat
    do alpha = 1, 3
      iden(alpha,alpha,i,i) = (1.0d0,0.0d0)
    end do 
  end do

  proj = iden

  do i = 1, 3
    proj = proj - gt(i,:,:,:,:)
  end do

      do i = 1, nat
        do j = 1, nat
          print *, i, j
          do alpha = 1, 3
            print '(3(2f12.8,2x))', proj(alpha,:,i,j)
          end do
        end do
      end do

  call fourtotwo ( proj, proj2)

  do i = 1, n
    call fourtotwo ( gh(i,:,:,:,:), gh2 )
    gh_aux = matmul ( proj2, matmul( gh2, proj2) )
    call twotofour ( gh_aux, gh(i,:,:,:,:))
  end do

  deallocate(iden, proj, gh2, proj2, gh_aux)

end subroutine project_generators_onto_translations

! This subroutine generates the three generators of the translations

subroutine generate_translation_generator ( gt )

  implicit none

  double complex, dimension(:,:,:,:,:), intent(out) :: gt

  integer :: nat
  integer :: n, i, j
  double complex, dimension(:,:), allocatable :: gt2
  double complex :: aux

  gt = (0.0d0,0.0d0)

  nat = size( gt,4 ) ! dimension 4 of this array

  allocate(gt2(3*nat,3*nat))

  do n = 1, 3
    do j = 1, nat
      do i = 1, nat
        gt(n,n,n,i,j) = (1.0d0,0.0d0) 
      end do 
    end do
    call fourtotwo ( gt(n,:,:,:,:), gt2 )
    aux = 1.d0 / dsqrt(dotprodmat( gt2, gt2 ))
    gt(n,:,:,:,:) = aux * gt(n,:,:,:,:) 
  end do 

  ! Normalize them

  do n = 1, 3
    call fourtotwo ( gt(n,:,:,:,:), gt2 )
    aux = 1.d0 / dsqrt(dotprodmat( gt2, gt2 ))
    gt(n,:,:,:,:) = aux * gt(n,:,:,:,:) 
  end do 

  deallocate(gt2)

end subroutine generate_translation_generator

! This subroutine passes the coefficients of the dynamical matrix 
! written in a matrix to an array

subroutine coefftwotone (nred,ctwo,cone)

  integer, dimension(:), intent(in) :: nred
  double precision, dimension(:,:), intent(in) :: ctwo
  double precision, dimension(:), intent(out) :: cone

  integer :: i, sigma, nq, ka

  nq = size(nred)
 
  ka = 0

  do i = 1, nq
    do sigma = 1, nred(i)
      ka = ka + 1
      cone(ka) = ctwo(i,sigma)
    end do  
  end do

end subroutine coefftwotone

! This subroutine passes the coefficients of the dynamical matrix 
! written in a matrix to an array and fixes which coefficients
! are fixed in the minimization because they belong of modes
! not interesting

subroutine coefftwotonemode (nred,nmured,ctwo,cone,fixedcoeff)

  integer, dimension(:), intent(in) :: nred, nmured
  double precision, dimension(:,:), intent(in) :: ctwo
  double precision, dimension(:), intent(out) :: cone
  logical, dimension(:), intent(out) :: fixedcoeff

  integer :: i, sigma, nq, ka

  nq = size(nred)
 
  ka = 0

  fixedcoeff = .false.

  do i = 1, nq
    do sigma = 1, nred(i)
      ka = ka + 1
      cone(ka) = ctwo(i,sigma)
      if (sigma .gt. nmured(i)) fixedcoeff(ka) = .true.  
    end do  
  end do

end subroutine coefftwotonemode

! This subroutine does the inverse to the previous one

subroutine coeffonetotwo (nred,cone,ctwo)

  integer, dimension(:), intent(in) :: nred
  double precision, dimension(:), intent(in) :: cone
  double precision, dimension(:,:), intent(out) :: ctwo

  integer :: i, sigma, nq, ka

  nq = size(nred)
 
  ka = 0

  do i = 1, nq
    do sigma = 1, nred(i)
      ka = ka + 1
      ctwo(i,sigma) = cone(ka)
    end do  
  end do 

end subroutine coeffonetotwo

! This subroutine creates the dynamical matrix making use of
! the generators and the coefficients that decompose it

subroutine generate_dyn(nred, coeff, ghr, dyn)

  integer, intent(in) :: nred
  double precision, dimension(:), intent(in) :: coeff
  double complex, dimension(:,:,:,:,:), intent(in) :: ghr
  double complex, dimension(:,:,:,:), intent(out) :: dyn
  
  integer :: i

  dyn = (0.0d0,0.0d0)
  
  do i = 1, nred
    dyn = dyn + coeff(i) * ghr(i,:,:,:,:)
  end do

end subroutine generate_dyn

! This subroutine performs the Gram-Schmidt orthogonalization
! of a basis form by matrices

subroutine gram_schmidt_mat ( g, gr, nred )

  implicit none

  double complex, dimension(:,:,:,:,:), intent(in) :: g
  double complex, dimension(:,:,:,:,:), intent(out) :: gr
  integer, intent(out) :: nred

  integer :: nspace, nat, nmode, counter
  integer :: i, j, k, ka
  double precision :: prec, aux
  double complex, dimension(:,:,:), allocatable :: g2, g2r
  double complex, dimension(:,:), allocatable :: mat, mat_aux     
  double precision, dimension(:), allocatable :: prodlist

  nspace = size(g(:,1,1,1,1))
  nat = size(g(1,1,1,:,1))  
  nmode = 3 * nat

  prec = 1.0d-4 

  gr = (0.0d0,0.0d0)

  allocate(g2(nspace,nmode,nmode))
  allocate(g2r(nspace,nmode,nmode))
  allocate(mat(nmode,nmode))
  allocate(mat_aux(nmode,nmode))
  allocate(prodlist(nspace))  

  do i = 1, nspace
    call fourtotwo(g(i,:,:,:,:),g2(i,:,:))
  end do

  ka = 0

  ! Create the basis using the Gram-Schmidt procedure

  do i = 1, nspace
    if ( ka .eq. 0) then
      counter = 0
      do j = 1, nmode
        do k = 1, nmode
          if ( abs( g2(i,j,k)) .gt. prec ) counter = counter + 1
        end do
      end do
      if ( counter .gt. 0 ) then
        ka = ka + 1
        aux = 1.d0 / dsqrt( dotprodmat(g2(i,:,:),g2(i,:,:)) )
        g2r(ka,:,:) = aux * g2(i,:,:) 
      end if
    else
      mat = g2(i,:,:)
      do j = 1, ka
        mat_aux =  dotprodmat(g2r(j,:,:),g2(i,:,:)) * g2r(j,:,:) 
        mat = mat - mat_aux
      end do
      counter = 0
      do j = 1, nmode
        do k = 1, nmode
          if ( abs( mat(j,k)) .gt. prec ) counter = counter + 1
        end do
      end do
      if ( counter .gt. 0 ) then
        ka = ka + 1
        aux = 1.d0 / dsqrt( dotprodmat(mat,mat))
        g2r(ka,:,:) = aux * mat 
      end if
    end if
  end do

  nred = ka

  do i = 1, nred
    call twotofour(g2r(i,:,:),gr(i,:,:,:,:))
  end do

  deallocate( g2, g2r, mat, mat_aux, prodlist ) 
  
end subroutine gram_schmidt_mat 

! This subroutine performs the Gram-Schmidt orthogonalization
! of a basis formed by matrices and according to the
! mode dependencies 

subroutine gram_schmidt_mat_mubase ( g, gr, mu_start, mu_end, nmured, nred )

  implicit none

  double complex, dimension(:,:,:,:,:), intent(in) :: g
  double complex, dimension(:,:,:,:,:), intent(out) :: gr
  integer, intent(in) :: mu_end, mu_start
  integer, intent(out) :: nmured, nred

  integer :: nspace, nat, nmode, counter, nmu
  integer :: i, j, k, ka, ku
  double precision :: prec, aux
  double complex, dimension(:,:,:), allocatable :: g2, g2r
  double complex, dimension(:,:), allocatable :: mat, mat_aux     
  double precision, dimension(:), allocatable :: prodlist

  nspace = size(g(:,1,1,1,1))
  nat = size(g(1,1,1,:,1))  
  nmode = 3 * nat
  nmu = (mu_end - mu_start + 1)**2

  prec = 1.0d-4 

  gr = (0.0d0,0.0d0)

  allocate(g2(nspace,nmode,nmode))
  allocate(g2r(nspace,nmode,nmode))
  allocate(mat(nmode,nmode))
  allocate(mat_aux(nmode,nmode))
  allocate(prodlist(nspace))  

  do i = 1, nspace
    call fourtotwo(g(i,:,:,:,:),g2(i,:,:))
  end do

  ka = 0
  ku = 0

  ! Create the basis using the Gram-Schmidt procedure

  do i = 1, nspace
    if ( ka .eq. 0) then
      counter = 0
      do j = 1, nmode
        do k = 1, nmode
          if ( abs( g2(i,j,k)) .gt. prec ) counter = counter + 1
        end do
      end do
      if ( counter .gt. 0 ) then
        ka = ka + 1
        aux = 1.d0 / dsqrt( dotprodmat(g2(i,:,:),g2(i,:,:)) )
        g2r(ka,:,:) = aux * g2(i,:,:) 
      end if
    else
      mat = g2(i,:,:)
      do j = 1, ka
        mat_aux =  dotprodmat(g2r(j,:,:),g2(i,:,:)) * g2r(j,:,:) 
        mat = mat - mat_aux
      end do
      counter = 0
      do j = 1, nmode
        do k = 1, nmode
          if ( abs( mat(j,k)) .gt. prec ) counter = counter + 1
        end do
      end do
      if ( counter .gt. 0 ) then
        ka = ka + 1
        aux = 1.d0 / dsqrt( dotprodmat(mat,mat))
        g2r(ka,:,:) = aux * mat 
      end if
    end if
    if ( i .ge. nmu .and. ku .eq. 0) then
      ku = ka
    end if
  end do

  nred = ka
  nmured = ku

  do i = 1, nred
    call twotofour(g2r(i,:,:),gr(i,:,:,:,:))
  end do

  deallocate( g2, g2r, mat, mat_aux, prodlist ) 
  
end subroutine gram_schmidt_mat_mubase

! This subroutine performs the Gram-Schmidt orthogonalization
! of a basis form by polarization vectors

subroutine gram_schmidt_vect ( e, er, nred)

  implicit none

  double complex, dimension(:,:), intent(in) :: e
  double complex, dimension(:,:), intent(out) :: er
  integer, intent(out) :: nred

  integer :: nspace, nat, nmode, counter
  integer :: i, j, k, ka, mu, alpha
  double precision :: prec
  double complex, dimension(:), allocatable :: mat, mat_aux     

  nmode  = size(e(1,:))
  nspace = size(e(:,1))

  prec = 1.0d-5 

  allocate(mat(nmode))
  allocate(mat_aux(nmode))

  ka = 0

  ! Create the basis using the Gram-Schmidt procedure

  do i = 1, nspace
    if ( ka .eq. 0) then
      counter = 0
      do j = 1, nmode
        if ( abs( e(i,j)) .gt. prec ) counter = counter + 1
      end do
      if ( counter .gt. 0 ) then
        ka = ka + 1
        er(ka,:) = e(i,:)  
      end if
    else
      mat = e(i,:)
      do j = 1, ka 
        mat_aux(:) =  dot_product(er(j,:),e(i,:)) * er(j,:) &
                    / dot_product(er(j,:),er(j,:))
        mat = mat - mat_aux
      end do
      counter = 0
      do j = 1, nmode
        if ( abs( mat(j)) .gt. prec ) counter = counter + 1
      end do  
      if ( counter .gt. 0 ) then
        ka = ka + 1
        er(ka,:) = mat  
      end if      
    end if
  end do

  nred = ka

  ! Normalize the basis

  do i = 1, nred
    er(i,:) = er(i,:) / dsqrt( abs(dot_product(er(i,:),er(i,:))) )
  end do

  deallocate( mat, mat_aux)  
  
end subroutine gram_schmidt_vect

! This subroutine performs the Gram-Schmidt orthogonalization
! of a basis form by real vectors of dimension (3,nat)

subroutine gram_schmidt_disp ( basis, basisr, nred)

  implicit none

  double precision, dimension(:,:,:), intent(in) :: basis
  double precision, dimension(:,:,:), intent(out) :: basisr
  integer, intent(out) :: nred

  integer :: nat, counter
  integer :: i, j, k, ka, n, alpha
  double precision :: prec
  double precision, dimension(:), allocatable :: mat, mat_aux
  double precision, dimension(:,:), allocatable :: f, fr     

  nat  = size(basis(1,1,:))

  prec = 1.0d-5 

  allocate(mat(3*nat))
  allocate(mat_aux(3*nat))
  allocate(f(3*nat,3*nat))
  allocate(fr(3*nat,3*nat))

  ! Write the vectors as a 1D vector

  do n = 1, 3*nat
    ka = 0
    do i = 1, nat
      do alpha = 1, 3
        ka = ka + 1
        f(n,ka) = basis(n,alpha,i)
      end do
    end do
  end do 

  ! Create the basis using the Gram-Schmidt procedure

  ka = 0

  do i = 1, 3*nat
    if ( ka .eq. 0) then
      counter = 0
      if ( dot_product(f(i,:),f(i,:)) .gt. prec ) counter = 1
!      do j = 1, 
!        if ( abs( e(i,j)) .gt. prec ) counter = counter + 1
!      end do
      if ( counter .gt. 0 ) then
        ka = ka + 1
        fr(ka,:) = f(i,:)  
      end if
    else
      mat = f(i,:)
      do j = 1, ka 
        mat_aux(:) =  dot_product(fr(j,:),f(i,:)) * fr(j,:) &
                    / dot_product(fr(j,:),fr(j,:))
        mat = mat - mat_aux
      end do
      counter = 0
      if ( dot_product(mat,mat) .gt. prec ) counter = 1
!      do j = 1, nmode
!        if ( abs( mat(j)) .gt. prec ) counter = counter + 1
!      end do  
      if ( counter .gt. 0 ) then
        ka = ka + 1
        fr(ka,:) = mat  
      end if      
    end if
  end do

  nred = ka

  ! Normalize the basis

  do i = 1, nred
    fr(i,:) = fr(i,:) / dsqrt( abs(dot_product(fr(i,:),fr(i,:))) )
  end do

  ! Write the reduced vector in (3,nat) format

  basisr = 0.0d0

  ka = 0

  do n = 1, nred
    ka = 0
    do i = 1, nat
      do alpha = 1, 3
        ka = ka + 1
        basisr(n,alpha,i) =  fr(n,ka)
      end do
    end do
  end do 

  deallocate( mat, mat_aux, f, fr)  
  
end subroutine gram_schmidt_disp

! This function calculates the trace of a matrix

function trace(a) result(result_trace)

  double precision, dimension(:,:), intent(in) :: a
  integer :: n, i
  double precision :: result_trace

  n = size(a(1,:))

  result_trace = 0.0d0

  do i = 1, n
    result_trace = result_trace + a(i,i)
  end do

end function trace

! This function calculates the dot product of
! two complex hermitian square matrices

function dotprodmat(a,b) result(result_dot)

  implicit none

  double complex, dimension(:,:), intent(in) :: a, b
  double complex, dimension(:,:), allocatable :: c
  integer :: n, i
  double precision :: result_dot
  double complex :: compl 

  n = size(a(1,:))

  allocate(c(n,n))

!  c = matmul(a,transpose(conjg(b)))


  ! Call lapack subroutine to calculate matrix product
  c = (0.0d0,0.0d0) 
  call zgemm('N','C',n,n,n,1.0d0,a,n,b,n,0.0d0,c,n)

  compl = (0.0d0,0.0d0)
 
  do i = 1, n
    compl = compl + c(i,i)
  end do

  result_dot = real(compl)
  
  deallocate(c)

end function dotprodmat

function dotprodmat_real(a,b) result(result_dot)

  implicit none

  double precision, dimension(:,:), intent(in) :: a, b
  double precision, dimension(:,:), allocatable :: c
  integer :: n, i
  double precision :: result_dot
  double precision :: trace 

  n = size(a(1,:))

  allocate(c(n,n))

!  c = matmul(a,transpose(conjg(b)))


  ! Call lapack subroutine to calculate matrix product
  c = 0.0d0
  call dgemm('N','C',n,n,n,1.0d0,a,n,b,n,0.0d0,c,n)

  trace = 0.0d0
 
  do i = 1, n
    trace = trace + c(i,i)
  end do

  result_dot = trace
  
  deallocate(c)
end function dotprodmat_real

! This subroutine calculates the product of two matrices
! given in the dimension (3,3,nat,nat).

subroutine dotprodmat4 (a,b,c)

  implicit none

  double complex, dimension(:,:,:,:), intent(in) :: a, b
  double precision, intent(out) :: c

  double complex, dimension(:,:), allocatable :: a2, b2
  integer :: nat

  nat = size (a(1,1,:,1))

  allocate(a2(3*nat,3*nat))
  allocate(b2(3*nat,3*nat))

  call fourtotwo(a,a2)
  call fourtotwo(b,b2)

  c = dotprodmat(a2,b2)

  deallocate(a2,b2)

end subroutine dotprodmat4

! This subroutine calculates the coefficients of a 
! hermitian matrix in terms of its generators 

subroutine project_dyn ( dyn, g, a )

  implicit none

  double complex, dimension(:,:,:,:), intent(in) :: dyn
  double complex, dimension(:,:,:,:,:), intent(in) :: g
  double precision, dimension(:), intent(out) :: a

  integer :: nred, nat, nmode
  double complex, dimension(:,:), allocatable :: dyn2, g2
  integer :: i

  nred = size(a)
  nat = size(dyn(1,1,:,1))
  nmode = 3*nat

  allocate(dyn2(nmode,nmode))
  allocate(g2(nmode,nmode)) 
  
  call fourtotwo(dyn, dyn2)

  do i = 1, nred
    call fourtotwo(g(i,:,:,:,:), g2)
    a(i) = dotprodmat(dyn2,g2) 
  end do

  deallocate( dyn2, g2)

end subroutine project_dyn

! This subroutine generates the basis of a set of 
! (3,3,nat,nat) hermitian matrices. The dimension of the
! group is (3*nat)**2. This subroutine creates all the 
! generators of the group.

subroutine generate_hermitian_basis ( nat, gh )

  implicit none

  integer, intent(in) :: nat
  double complex, dimension(:,:,:,:,:), intent(out) :: gh

  double complex, dimension(:,:), allocatable :: gh2
  integer :: n, ng, i, mu, nu
  double precision :: const

  n = 3 * nat

  gh = (0.0d0,0.0d0)

  const = 0.70710678118654746d0

  allocate(gh2(n,n))

  ng = 0

  ! First matrices with ones in the diagonal

  do i = 1, n 
    gh2 = (0.0d0,0.0d0)
    gh2 ( i, i ) = (1.0d0,0.0d0)
    ng = ng + 1
    call twotofour(gh2,gh(ng,:,:,:,:))
  end do

  ! Second matrices with 1/sqrt(2) in the offdiagonals

  do mu = 1, n
    do nu = mu+1, n
      gh2 = (0.0d0,0.0d0)
      gh2 ( mu, nu) = const * (1.0d0,0.0d0)
      gh2 ( nu, mu) = const * (1.0d0,0.0d0)
      ng = ng + 1
      call twotofour(gh2,gh(ng,:,:,:,:))
    end do
  end do

  ! Finally matrices with i/sqrt(2) in the offdiagonals

  do mu = 1, n
    do nu = mu+1, n
      gh2 = (0.0d0,0.0d0)
      gh2 ( mu, nu) = const * (0.0d0,1.0d0)
      gh2 ( nu, mu) = - const * (0.0d0,1.0d0)
      ng = ng + 1
      call twotofour(gh2,gh(ng,:,:,:,:))
    end do
  end do

  deallocate(gh2)
  
end subroutine generate_hermitian_basis

! This subroutine generates the basis of a set of 
! (3,3,nat,nat) hermitian matrices. The dimension of the
! group is (3*nat)**2. This subroutine creates all the 
! generators of the group. In this case the basis is 
! is created from the polarization vectors

subroutine generate_hermitian_basis_from_e ( nat, mu_start, mu_end, e, gh )

  implicit none

  integer, intent(in) :: nat, mu_start, mu_end
  double complex, dimension(:,:,:), intent(in) :: e
  double complex, dimension(:,:,:,:,:), intent(out) :: gh

  integer :: ng, nmu, nmug, mark
  integer :: n, i, j, mu, nu, alpha, beta

  n = 3 * nat
  nmu = mu_end - mu_start + 1

  gh = (0.0d0,0.0d0)

  ng = nmu*nmu
  nmug = 0

  do mu = 1, n
    do nu = 1, n
      if (mu .ge. mu_start .and. mu .le. mu_end .and. nu .ge. mu_start .and. nu .le. mu_end ) then
        nmug = nmug + 1
        mark = nmug
      else
        ng = ng + 1
        mark = ng
      end if
      do i = 1, nat
        do j = 1, nat
          do alpha = 1, 3
            do beta = 1, 3
              gh(mark,alpha,beta,i,j) = e(mu,i,alpha) * conjg(e(nu,j,beta)) 
            end do
          end do
        end do
      end do
    end do
  end do

end subroutine generate_hermitian_basis_from_e

! This subroutine generates the basis of a set of 
! (3,3,nat,nat) hermitian matrices. The dimension of the
! group is (3*nat)**2. This subroutine creates all the 
! generators of the group. In this case the basis is 
! is created from the polarization vectors.
! CORRECTED VERSION!

subroutine generate_hermitian_basis_from_e_new ( nat, mu_start, mu_end, e, gh )

  implicit none

  integer, intent(in) :: nat, mu_start, mu_end
  double complex, dimension(:,:,:), intent(in) :: e
  double complex, dimension(:,:,:,:,:), intent(out) :: gh

  integer :: ng, nmu, nmug, mark
  integer :: i, j, mu, nu, alpha, beta
  double precision :: const
  double complex :: im

  const = 0.70710678118654746d0
  im = (0.0d0,1.0d0)

  nmu = mu_end - mu_start + 1

  gh = (0.0d0,0.0d0)

  ng = nmu * nmu
  nmug = 0

  ! First matrices formed with e(mu) e(mu)*

  do mu = 1, 3*nat
    if (mu .ge. mu_start .and. mu .le. mu_end) then
      nmug = nmug + 1
      mark = nmug
    else
      ng = ng + 1
      mark = ng
    end if
    do i = 1, nat
      do j = 1, nat
        do alpha = 1, 3
          do beta = 1, 3
            gh(mark,alpha,beta,i,j) = e(mu,i,alpha) * conjg(e(mu,j,beta))
          end do
        end do
      end do
    end do
  end do

  !  matrices formed with [ e(mu) e(nu)* + e(nu) e(mu)* ] / sqrt(2) 

  do mu = 1, 3*nat
    do nu = mu+1, 3*nat
      if (mu .ge. mu_start .and. mu .le. mu_end .and. nu .ge. mu_start .and. nu .le. mu_end ) then
        nmug = nmug + 1
        mark = nmug
      else
        ng = ng + 1
        mark = ng
      end if
      do i = 1, nat
        do j = 1, nat
          do alpha = 1, 3
            do beta = 1, 3
              gh(mark,alpha,beta,i,j) = ( e(mu,i,alpha) * conjg(e(nu,j,beta)) + &
                                          e(nu,i,alpha) * conjg(e(mu,j,beta)) ) * const
            end do
          end do
        end do
      end do
    end do
  end do

  ! Third matrices formed with [ e(mu) e(nu)* - e(nu) e(mu)* ] i / sqrt(2) 

  do mu = 1, 3*nat
    do nu = mu+1, 3*nat
      if (mu .ge. mu_start .and. mu .le. mu_end .and. nu .ge. mu_start .and. nu .le. mu_end ) then
        nmug = nmug + 1
        mark = nmug
      else
        ng = ng + 1
        mark = ng
      end if
      do i = 1, nat
        do j = 1, nat
          do alpha = 1, 3
            do beta = 1, 3
              gh(mark,alpha,beta,i,j) = ( e(mu,i,alpha) * conjg(e(nu,j,beta)) - &
                                          e(nu,i,alpha) * conjg(e(mu,j,beta)) ) * const * im
            end do
          end do
        end do
      end do
    end do
  end do

  ! Test if all generators were created

  if (ng .ne. 9*nat*nat) then
    print *, ''
    print *, ' ERROR: The number of generators created does not expand'
    print *, '        the full hermitian basis.                       '
    print *, '        '
    print *, ng, 9*nat*nat
    print *, '        '
    print *, '        Stopping...                                     '
    print *, ''
    stop
  end if

end subroutine generate_hermitian_basis_from_e_new

! This subroutine creates a basis for 3n size real
! vectors

subroutine generate_displacement_basis ( nat, basis_disp )

  implicit none

  integer, intent(in) :: nat
  double precision, dimension(:,:,:), intent(out) :: basis_disp

  integer :: n, i, alpha
  double precision, dimension(3,nat) :: f

  n = 0 

  do i = 1, nat
    do alpha = 1, 3
      n = n + 1
      f = 0.0d0
      f(alpha,i) = 1.0d0
      basis_disp(n,:,:) = f(:,:)
    end do
  end do

end subroutine generate_displacement_basis

! This subroutine writes a (3,3,nat,nat) complex matrix in the
! (3*nat,3*nat) 

subroutine fourtotwo (matfour,mattwo)

  implicit none

  double complex, dimension(:,:,:,:), intent(in) :: matfour   
  double complex, dimension(:,:), intent(out) :: mattwo   

  integer :: nat
  integer :: i, j, alpha, beta

  nat = size(matfour(1,1,:,1))

  do j = 1, nat
    do i = 1, nat
      do beta = 1, 3
        do alpha = 1, 3
          mattwo(3*(i-1)+alpha,3*(j-1)+beta) = matfour(alpha,beta,i,j)
        end do   
      end do
    end do
  end do

end subroutine fourtotwo


subroutine fourtotwo_real (matfour,mattwo)

  implicit none

  double precision, dimension(:,:,:,:), intent(in) :: matfour   
  double precision, dimension(:,:), intent(out) :: mattwo   

  integer :: nat
  integer :: i, j, alpha, beta

  nat = size(matfour(1,1,:,1))

  do j = 1, nat
    do i = 1, nat
      do beta = 1, 3
        do alpha = 1, 3
          mattwo(3*(i-1)+alpha,3*(j-1)+beta) = matfour(alpha,beta,i,j)
        end do   
      end do
    end do
  end do

end subroutine fourtotwo_real

! This subroutine writes a (3*nat,3*nat) complex matrix in the
! (3,3,nat,nat) 

subroutine twotofour (mattwo,matfour)

  implicit none

  double complex, dimension(:,:), intent(in) :: mattwo   
  double complex, dimension(:,:,:,:), intent(out) :: matfour   

  integer :: nat
  integer :: i, j, alpha, beta

  nat = size(matfour(1,1,:,1))

  do j = 1, nat
    do i = 1, nat
      do beta = 1, 3
        do alpha = 1, 3
          matfour(alpha,beta,i,j) = mattwo(3*(i-1)+alpha,3*(j-1)+beta)     
        end do   
      end do
    end do
  end do

end subroutine twotofour

! This subroutine writes a (3*nat,3*nat) real matrix in the
! (3,3,nat,nat) 

subroutine twotofour_real (mattwo,matfour)

  implicit none

  double precision, dimension(:,:), intent(in) :: mattwo
  double precision, dimension(:,:,:,:), intent(out) :: matfour

  integer :: nat
  integer :: i, j, alpha, beta

  nat = size(matfour(1,1,:,1))

  do j = 1, nat
    do i = 1, nat
      do beta = 1, 3
        do alpha = 1, 3
          matfour(alpha,beta,i,j) = mattwo(3*(i-1)+alpha,3*(j-1)+beta)
        end do
      end do
    end do
  end do

end subroutine twotofour_real

! This subroutine writes a (3*nat,3*nat,3*nat) real matrix in the
! (nat,nat,nat,3,3,3) 

subroutine threetosix_real (mat3,mat6)

  implicit none

  double precision, dimension(:,:,:), intent(in) :: mat3
  double precision, dimension(:,:,:,:,:,:), intent(out) :: mat6

  integer :: nat
  integer :: i, j, k, alpha, beta, gamm

  nat = size(mat3(:,1,1)) / 3

  do k = 1, nat
    do j = 1, nat
      do i = 1, nat
        do gamm = 1, 3
          do beta = 1, 3
            do alpha = 1, 3
              mat6(i,j,k,alpha,beta,gamm) = mat3(3*(i-1)+alpha,3*(j-1)+beta,3*(k-1)+gamm)
            end do
          end do
        end do
      end do
    end do
  end do

end subroutine threetosix_real

! This subroutine writes a (3*nat,3*nat,3*nat) real matrix in the
! (nat,nat,nat,3,3,3) 

subroutine sixtothree_real (mat6,mat3)

  implicit none

  double precision, dimension(:,:,:,:,:,:), intent(in) :: mat6
  double precision, dimension(:,:,:), intent(out) :: mat3

  integer :: nat
  integer :: i, j, k, alpha, beta, gamm

  nat = size(mat3(:,1,1)) / 3

  do k = 1, nat
    do j = 1, nat
      do i = 1, nat
        do gamm = 1, 3
          do beta = 1, 3
            do alpha = 1, 3
              mat3(3*(i-1)+alpha,3*(j-1)+beta,3*(k-1)+gamm) = mat6(i,j,k,alpha,beta,gamm)
            end do
          end do
        end do
      end do
    end do
  end do

end subroutine sixtothree_real

! The following function select if a double precision is nan or not
function is_nan(guess) result (res)
  double precision, intent(in) ::  guess
  logical ::  res

  res = .false.
  if (guess /= guess) res = .true.
end function is_nan

! This subroutine calculates which is the -q vector of each q
! in the grid

subroutine set_minusq_list (q, bg, minusq_list)

  implicit none

  double precision, dimension(:,:), intent(in) :: q
  double precision, dimension(3,3), intent(in) :: bg
  integer, dimension(:), intent(out) :: minusq_list

  double precision, dimension(27,3) :: g_vectors
  double precision, dimension(3) :: vect
  integer :: l, i, j, k
  integer :: nq
  double precision :: prec

  ! Get number of q points

  nq = size(q(1,:))

  ! Threshold value to say whether two vectors are the same

  prec = 1.0d-4

  ! Create reciprocal lattice vectors

  l = 1

  do i = -1, 1
    do j = -1, 1
      do k = -1, 1
        g_vectors(l,:) = dble(i) * bg(:,1) + dble(j) * bg(:,2) + dble(k) * bg(:,3)
        l = l + 1
      end do
    end do
  end do

  ! Assign -q vector for each q in the grid

  do i = 1, nq
    do j = 1, nq
      do l = 1, 27
        vect(:) = q(:,i) + q(:,j) - g_vectors(l,:)
        if (dot_product(vect,vect) .lt. prec) minusq_list(i) = j
      end do
    end do
  end do

end subroutine set_minusq_list

! For a given qirr vectors of the irreducible BZ
! this subroutine calculates which is the q vector
! in the total list

subroutine set_qirr_list (qirr, q, qirr_list)

  implicit none

  double precision, dimension(:,:), intent(in) :: qirr, q
  integer, dimension(:), intent(out) :: qirr_list

  double precision, dimension(3) :: vect
  integer :: l, i, j, k
  integer :: nq, nqirr
  double precision :: prec

  ! Get number of q points

  nq    = size(q(1,:))
  nqirr = size(qirr(1,:))

  ! Threshold value to say whether two vectors are the same

  prec = 1.0d-4

  ! Assign -q vector for each q in the grid

  do i = 1, nqirr
    do j = 1, nq
      vect(:) = qirr(:,i) - q(:,j)
      if (dot_product(vect,vect) .lt. prec) qirr_list(i) = j
    end do
  end do

end subroutine set_qirr_list

end module tools
