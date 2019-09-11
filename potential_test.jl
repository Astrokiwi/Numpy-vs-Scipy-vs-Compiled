"""
    softened_potential_threeloop(r,h)

Completely unrolled potential sum.

I have found this is the only version that gives comparable performance
to C/Fortran/etc, but it is more verbose than you'd hope
"""
function softened_potential_threeloop(r,h)
    N = size(r)[1]
    pot = 0.
    h2 = h^2
    @inbounds for i=1:N-1
        for j=i+1:N
            d=0.
            for k=1:3
                @views d+=(r[i,k]-r[j,k]).^2
            end
            d+=h2
            d = sqrt(d)^-1
            pot+=d
        end
    end
    return pot
end

"""
    softened_potential_twoloop(r,h)

Partially unrolled potential sum.

The innermost loop adds two 3-vectors. Julia creates a lot of intermediate
vectors here and it gets slow.
"""
function softened_potential_twoloop(r,h)
    # simple unwrapped loop
    N = size(r)[1]
    pot = 0.
    h2 = h^2
    @inbounds for i=1:N-1
        for j=i+1:N
            @views pot+=sqrt((sum((r[i,:].-r[j,:]).^2).+h2)).^-1
        end
    end
    return pot
end

"""
    softened_potential_oneloop(r,h)

The most concise potential sum, only using vector notation as you would in numpy etc

This creates some intermediate values, but oddly creates fewer than the twoloop version.
This may be a reasonable compromise between speed and simplicity. It's slower than a
simple Fortran loop, and comparable to the same algorithm in numpy.
"""
function softened_potential_oneloop(r,h)
    # vector operations
    n = size(r)[1]
    pot = 0.
    h2 = h^2
    @inbounds for i=1:N-1
        @views pot+=sum(sqrt.((sum((r[i,:]'.-r[i+1:N,:]).^2,dims=2).+h2)).^-1)
    end
    return pot
end


using Random

N = parse(Int64,ARGS[1])
r = Random.rand(N,3)
h = 0.01

println("N=",N)

# run twice, so timing isn't dominated by compile time
for i=1:2
    if i==1
        println("First Julia run to compile everything")
    else
        println("Julia run, with everything compiled (hopefully)")
    end
    print("julia threeloop")
    @time softened_potential_threeloop(r,h)
    print("julia twoloop")
    @time softened_potential_twoloop(r,h)
    print("julia oneloop")
    @time softened_potential_oneloop(r,h)
end