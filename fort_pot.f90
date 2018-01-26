module fort_pot
    contains
        function two_loop_pot(r,soft,N) result(pot)
            implicit none
            
            integer :: N
            real(kind=8), dimension(N,3) :: r
            real(kind=8) :: soft
            
            real(kind=8) :: pot

            integer :: i,j
            real(kind=8) :: soft2,dr
            
            soft2 = soft**2
            pot = 0.d0
            
            do i=1,N-1
                do j=i+1,N
                    dr = sqrt(sum((r(i,:)-r(j,:))**2)+soft2)
                    pot = pot + 1./dr
                end do
            end do
            return
        end function
        
        
        function fortran_sum(r,N) result(fsum)
            implicit none
            
            integer :: N
            real(kind=8), dimension(N,3) :: r
            real(kind=8) :: fsum
            
            integer :: i,j
            
            fsum = 0.
            
            do i=1,N
                fsum = fsum + sum(r(i,:))
            end do
            
            return
        end function

end module fort_pot