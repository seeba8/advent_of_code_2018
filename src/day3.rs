#[derive(Debug, PartialEq, Eq)]
pub struct Claim {
    id: usize,
    x: usize,
    y: usize,
    w: usize,
    h: usize
}
use regex::Regex;

#[aoc_generator(day3)]
pub fn input_generator(input: &str) -> Vec<Claim> {
    let mut claims: Vec<Claim> = Vec::new();
    let re = Regex::new(r"^#(\d+)\s@\s(\d+),(\d+):\s(\d+)x(\d+)$").unwrap();
    for l in input.lines() {
        let cap = match re.captures(l) {
            None => continue,
            Some(x) => x
        };

        claims.push(Claim{
            // cap[0] is the whole match
            id: cap[1].parse().expect(&cap[0]),
            x: cap[2].parse().expect("x broken"),
            y: cap[3].parse().expect("y broken"),
            w: cap[4].parse().expect("w broken"),
            h: cap[5].parse().expect("h broken")
        });
    }
    claims
}

#[aoc(day3, part1)]
pub fn solve_part1(input: &[Claim]) -> usize {
    let mut cloth = [0u8; 1_000_000];
    for claim in input.iter() {
        for w in 0usize..claim.w {
            for h in 0usize..claim.h {
                cloth[(claim.x+w)*1000 + claim.y+h] += 1;
            }
        }
    }
    cloth.iter().map(|&c| if c > 1 { 1 } else { 0 }).sum()


}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_inputparse() {
        assert_eq!(input_generator(r"
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
            "), &[Claim { id: 1, x: 1, y: 3, w: 4, h: 4 },
                  Claim { id: 2, x: 3, y: 1, w: 4, h: 4 },
                  Claim { id: 3, x: 5, y: 5, w: 2, h: 2 }
        ])
    }

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(
            &[Claim { id: 1, x: 1, y: 3, w: 4, h: 4 },
            Claim { id: 2, x: 3, y: 1, w: 4, h: 4 },
            Claim { id: 3, x: 5, y: 5, w: 2, h: 2 }
        ]), 4);
    }
}