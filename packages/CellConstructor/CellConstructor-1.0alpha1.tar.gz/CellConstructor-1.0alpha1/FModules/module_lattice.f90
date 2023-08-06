module lattice

public :: gvectors
public :: asign_supercell_index
public :: wyckoff_to_tau
public :: wyckoff_to_tau_sc

contains

! This subroutine assigns nearest neighbors if an atom in a 
! supercell in a fcc lattice

subroutine assign_NN (tau_sc, at_sc, ityp_sc, nn_at, nn_vect)

  implicit none

  integer, dimension(:), intent(in) :: ityp_sc
  double precision, dimension(:,:), intent(in) :: tau_sc, at_sc
  integer, dimension(:,:), intent(out) :: nn_at  
  double precision, dimension(:,:,:), intent(out) :: nn_vect

  integer,parameter :: far =2
  double precision, dimension((2*far+1)**3,3) :: t_vectors
  double precision, dimension(3) :: vect
  integer :: natsc
  integer :: i, k, j, l
  double precision :: nn_dist, dist

  natsc = size(tau_sc(1,:))

  ! Distance between nearest neighbors

  nn_dist = 0.5d0

  ! Create supercell lattice vectors

  l = 1

  do i = -far,far  
    do j = -far,far    
      do k = -far,far   
        t_vectors(l,:) = dble(i) * at_sc(:,1) + dble(j) * at_sc(:,2) + dble(k) * at_sc(:,3)
        l = l + 1    
      end do
    end do
  end do

  nn_at = 0

  do i = 1, natsc
    k = 0  
    do j = 1, natsc
      do l = 1, (2*far+1)**3
        vect(:) = tau_sc(:,i)-tau_sc(:,j)-t_vectors(l,:)
        dist = dsqrt(dot_product(vect(:),vect(:))) 
        if ( abs(dist - nn_dist) .lt. 1.0d-5 ) then
          k = k + 1
          nn_at(i,k) = j
          nn_vect(i,k,:) = vect(:)
        end if   
      end do 
    end do
    if (k .ne. 6) then
      print *, ' Not all or too many NN assigned', k
      stop
    end if
  end do

end subroutine assign_NN

subroutine assign_PM(nat_sc, index_vect, index_mat, slv_idx)
  use kinds, only: DP
  implicit none
  integer,intent(IN)   :: nat_sc
  real(DP), intent(IN) :: index_vect(nat_sc,6,3)
  integer,intent(IN)   :: index_mat(nat_sc,6)
  integer,intent(OUT) :: slv_idx(nat_sc,6)

  real(DP) :: dist(3)
  integer :: i,j, jj, is
  real(DP) ::  special(3,6), proj, aux

  special(:,1) = (/ 1.d0, 0.d0, 0.d0 /)
  special(:,2) = (/-1.d0, 0.d0, 0.d0 /)
  special(:,3) = (/ 0.d0, 1.d0, 0.d0 /)
  special(:,4) = (/ 0.d0,-1.d0, 0.d0 /)
  special(:,5) = (/ 0.d0, 0.d0, 1.d0 /)
  special(:,6) = (/ 0.d0, 0.d0,-1.d0 /)


  do i = 1,nat_sc
  write(*,*) "neighbours of atom", i
  do is = 1,6 ! six special directions
    proj = 0.d0
    do jj = 1,6 ! first neighbours
      j = index_mat(i,jj)
!       dist(:) = (coords(j,:)+atom_transl(i,j,:)) - coords(i,:)
!       dist(:) = (coords(j,:)+(tau_sc(:,j)-tau_sc(:,i)) - coords(i,:)
      dist(:) = index_vect(i,jj,:)
      aux = SUM( dist*special(:,is) )
      IF( aux > proj ) THEN
        proj = aux
        slv_idx(i,is) = j
      ENDIF

    enddo
   write(*,'(2(a,i3),2(a,3f10.4))') "type", is, " idx", slv_idx(i, is) 
  enddo
  enddo

end subroutine assign_PM




! This subroutine assigns the supercell indices to the 
! atom positions in a supercell

subroutine asign_supercell_index(x_atom,x_atoms_prim,primlatt_vec,supercell_size,s,l,m,n)

  double precision, dimension(:), intent(in) :: x_atom
  double precision, dimension(:,:), intent(in) :: x_atoms_prim     
  double precision, dimension(3,3), intent(in) :: primlatt_vec     
  integer, dimension(3), intent(in) :: supercell_size
  integer, intent(out) :: s
  integer, intent(out) :: l
  integer, intent(out) :: m
  integer, intent(out) :: n

  double precision, dimension(3,3) :: matrix
  double precision, dimension(3) :: vector
  integer, dimension(3) :: ipiv
  integer :: i, j, natoms_prim, info
  character (len=3) :: logi

  natoms_prim = size(x_atoms_prim(1,:))
  
  do j = 1, natoms_prim
!    matrix = transpose(primlatt_vec)
    matrix = primlatt_vec
    vector(:) = x_atom(:) - x_atoms_prim(:,j)
    call dgetrf(3,3,matrix,3,ipiv,info)
    call dgetrs('N',3,3,matrix,3,ipiv,vector,3,info) 
    call integer_test(vector,supercell_size,logi)
    if (logi .eq. 'yes') then
      s = j
      l = int(vector(1)) + 1
      m = int(vector(2)) + 1
      n = int(vector(3)) + 1
    end if
  end do

end subroutine asign_supercell_index

! This subroutine assigns the supercell indices to the 
! atom positions in a supercell

subroutine asign_supercell_index_new(vect,at,l,m,n)

  double precision, dimension(3), intent(in) :: vect
  double precision, dimension(3,3), intent(in) :: at               
  integer, intent(out) :: l
  integer, intent(out) :: m
  integer, intent(out) :: n

  double precision, dimension(3,3) :: matrix
  double precision, dimension(3) :: vector
  integer, dimension(3) :: ipiv
  integer :: i, j, info
  character (len=3) :: logi

  matrix = at           
  call dgetrf(3,3,matrix,3,ipiv,info)
  call dgetrs('N',3,3,matrix,3,ipiv,vect,3,info) 
  l = nint(vect(1)) + 1
  m = nint(vect(2)) + 1
  n = nint(vect(3)) + 1

end subroutine asign_supercell_index_new

! This subroutine tests wether a vector is formed by
! integer numbers or not

subroutine integer_test(vector,supercell_size,logi)

  double precision, dimension(3), intent(in) :: vector
  integer, dimension(3), intent(in) :: supercell_size
  character (len=3), intent(out) :: logi

  integer :: i, j, k

  logi = 'non'

  do i = 0, supercell_size(1)
    if (vector(1)-dble(i) .eq. 0.0d0) then
      do j = 0, supercell_size(2)
        if (vector(2)-dble(j) .eq. 0.0d0) then
          do k = 0, supercell_size(3)
            if (vector(3)-dble(k) .eq. 0.0d0) then
              logi = 'yes'
            end if
          end do
        end if
      end do
    end if
  end do    

end subroutine integer_test

! This subroutine calculates the atomic positions in 
! alat cartesian coordinates from the free parameters in the
! Wyckoff positions

subroutine wyckoff_to_tau( chi, chi_wyckoff, wyckoff_coeff, tau ) 

  implicit none

  double precision, dimension(:,:), intent(in) :: chi
  double precision, dimension(:,:,:), intent(in) :: chi_wyckoff
  double precision, dimension(:), intent(in) :: wyckoff_coeff 
  double precision, dimension(:,:), intent(out) :: tau

  integer :: n_wyckoff, nat
  integer :: i, j

  n_wyckoff = size(wyckoff_coeff)
  nat = size(chi(1,:))

  tau = chi

  do i = 1, n_wyckoff
    do j = 1, nat
      tau(:,j) = tau(:,j) + wyckoff_coeff(i) * chi_wyckoff(i,:,j)   
    end do
  end do  

end subroutine wyckoff_to_tau

! This subroutine calculates the atomic positions in 
! alat cartesian coordinates from the free parameters in the
! Wyckoff positions for the supercell

subroutine wyckoff_to_tau_sc( chi, chi_wyckoff, wyckoff_coeff, itau, tau ) 

  implicit none

  double precision, dimension(:,:), intent(in) :: chi
  double precision, dimension(:,:,:), intent(in) :: chi_wyckoff
  double precision, dimension(:), intent(in) :: wyckoff_coeff 
  integer, dimension(:), intent(in) :: itau
  double precision, dimension(:,:), intent(out) :: tau

  integer :: n_wyckoff, nat
  integer :: i, j

  n_wyckoff = size(wyckoff_coeff)
  nat = size(chi(1,:))

  tau = chi

  do i = 1, n_wyckoff
    do j = 1, nat
      tau(:,j) = tau(:,j) + wyckoff_coeff(i) * chi_wyckoff(i,:,itau(j))   
    end do
  end do  

end subroutine wyckoff_to_tau_sc

! This subroutine calculates which atom in the supercell
! is related by a translation vector of the supercell 
! to another atom of the supercell

subroutine get_tau_sc_latvec ( tau_sc, latvec, at_sc, tau_sc_latvec )

  implicit none

  double precision, dimension(:,:), intent(in) :: tau_sc, latvec 
  double precision, dimension(3,3), intent(in) :: at_sc
  integer, dimension(:,:), intent(out) :: tau_sc_latvec

  integer :: nr, nat_sc
  double precision, dimension(3) :: diff
  double precision, dimension(27,3) :: superlatvec
  double precision :: prec
   
  integer :: ka, i, j, k, r

  ! Define precision for scalar product that
  ! decides if two positions are the same

  prec = 1.0d-6

  ! Get integers

  nr = size(latvec(:,1))
  nat_sc = size(tau_sc(1,:))

  ! Create the supercell lattice vectors

  ka = 0

  do i = -1, 1
    do j = -1, 1
      do k = -1, 1
        ka = ka + 1
        superlatvec(ka,:) = dble(i) * at_sc(:,1) + dble(j) * at_sc(:,2) + dble(k) * at_sc(:,3)
      end do
    end do
  end do

  ! Calculate which is the atom of the supercell related to a given 
  ! lattice vector

  do i = 1, nat_sc
    do r = 1, nr
      do j = 1, nat_sc
        do ka = 1, 27   
          diff(:) = tau_sc(:,i) + latvec(r,:) - tau_sc(:,j) + superlatvec(ka,:)
          if (dot_product(diff,diff) .lt. prec) then
            tau_sc_latvec(i,r) = j
            print *, ''
            print '(a,i3,a,3f16.8)', ' Supercell atom ', i, ' : ', tau_sc(:,i)
            print '(a,i3,a,3f16.8)', ' Translation    ', r, ' : ', latvec(r,:)
            print '(a,i3,a,3f16.8)', ' Translate atom ', j, ' : ', tau_sc(:,j)
          end if
        end do
      end do
    end do
  end do

end subroutine get_tau_sc_latvec

end module lattice
