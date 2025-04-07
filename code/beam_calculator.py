class Beam:
    def __init__(self, length):
        self.length = length

    def single_point_load(self, W, x):
        L = self.length
        R_A = W * (L - x) / L
        R_B = W * x / L
        return R_A, R_B
    
    def bending_moment_one(self, load, position):
        L = self.length
        a = position
        b = L - a
        return load * a * b / L
    
    def shear_force_at(self, loads, position):
   
        L = self.length

    # Step 1: Calculate support reactions assuming simply supported beam
    # Summing moments about A to find R_B
        moment_sum = sum([W * x for x, W in loads])
        total_load = sum([W for _, W in loads])
        R_B = moment_sum / L
        R_A = total_load - R_B

    # Step 2: Shear force just to the left of the position
        SF = R_A
        for x, W in loads:
            if x < position:
                SF -= W
        return SF


    def shear_force_single(self, W, x, p):
        R_A, _ = self.single_point_load(W, x)
        if p < x:
            return R_A
        elif p == x:
            return R_A  # before the load is applied
        else:
            return R_A - W

    def bending_moment_single(self, W, x, p):
        R_A, _ = self.single_point_load(W, x)
        if p < x:
            return R_A * p
        else:
            return R_A * p - W * (p - x)

    def max_shear_bending_single(self, W, x):
        R_A, _ = self.single_point_load(W, x)
        max_shear = max(abs(R_A), abs(R_A - W))
        max_bm_pos = R_A / W * self.length
        max_bm = self.bending_moment_single(W, x, max_bm_pos)
        return max_shear, max_bm, max_bm_pos

    def two_point_load(self, W1, x1, W2, x):
        L = self.length
        x2 = x1 + x
        R_A = (W1 * (L - x1) + W2 * (L - x2)) / L
        R_B = (W1 * x1 + W2 * x2) / L
        return R_A, R_B, x2

    def shear_force_two(self, W1, x1, W2, x, p):
        R_A, _, x2 = self.two_point_load(W1, x1, W2, x)
        if p < x1:
            return R_A
        elif p < x2:
            return R_A - W1
        else:
            return R_A - W1 - W2

    def bending_moment_two(self, W1, x1, W2, x, p):
        R_A, _, x2 = self.two_point_load(W1, x1, W2, x)
        if p < x1:
            return R_A * p
        elif p < x2:
            return R_A * p - W1 * (p - x1)
        else:
            return R_A * p - W1 * (p - x1) - W2 * (p - x2)

    def max_reactions_moving_load(self, W1, W2, x):
        L = self.length
        R_A = W1 + W2 * (L - x) / L
        R_B = W2 + W1 * (L - x) / L
        return R_A, R_B

    def shear_at_position(self, W1, x1, W2, x, position):
        return self.shear_force_two(W1, x1, W2, x, position)

    def max_shear_moment(self, W1, W2, x, step=0.1):
        L = self.length
        max_sf, max_bm = float("-inf"), float("-inf")
        max_sf_pos, max_bm_pos = 0, 0

        pos_range = [round(p, 4) for p in self._frange(0, L - x, step)]
        for x1 in pos_range:
            sf = self.shear_at_position(W1, x1, W2, x, L/2)
            bm = self.bending_moment_two(W1, x1, W2, x, L/2)

            if abs(sf) > max_sf:
                max_sf = abs(sf)
                max_sf_pos = x1

            if bm > max_bm:
                max_bm = bm
                max_bm_pos = x1

        return max_sf, max_sf_pos, max_bm, max_bm_pos

    def _frange(self, start, stop, step):
        while start <= stop:
            yield round(start, 4)
            start += step
