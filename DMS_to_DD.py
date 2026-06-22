#Make sure raw is a string that contains a single coordinate in DMS form
def convert(raw):
    n,w = raw.split(" ")
    n = [int(p) for p in n.split(",")]
    w = [int(p) for p in w.split(",")]
    north, west = 0,0
    for i in range(3): 
        north += n[i]*(1/60**i)
        west -= w[i]*(1/60**i)
    return [north,west]
