function softened_potential_threeloop(r,h)
    # simple unwrapped loop
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

# run twice, so timing isn't dominated by compile time
for i=1:2
    print("julia threeloop")
    @time softened_potential_threeloop(r,h)
    print("julia twoloop")
    @time softened_potential_twoloop(r,h)
    print("julia oneloop")
    @time softened_potential_oneloop(r,h)
end