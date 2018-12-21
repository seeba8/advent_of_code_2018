use std::collections::HashSet;

#[aoc_generator(day1)]
pub fn input_generator(input: &str) -> Vec<isize> {
    input
        .lines()
        .map(|l| {
            l.trim().parse().unwrap()
        })
        .collect()
}

#[aoc(day1, part1)]
pub fn solve_part1(input: &[isize]) -> isize {
    input.iter().sum()
}

#[aoc(day1, part2)]
pub fn solve_part2(input: &[isize]) -> isize {
    let mut current_freq: isize = 0;
    let mut seen_frequencies = HashSet::new();
    seen_frequencies.insert(0 as isize);
    loop {
        for next_freq in input.iter() {
            current_freq += next_freq;
            if seen_frequencies.contains(&current_freq) {
                return current_freq
            }
            else {
                seen_frequencies.insert(current_freq);
            }
        }
    }
}


#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_inputparse() {
        assert_eq!(input_generator("+1\n-2\n+3456234"), [1, -2, 3456234]);
    }

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(&[1,14]), 15);
        assert_eq!(solve_part1(&[1,14,-5]), 10);
        assert_eq!(solve_part1(&[5,-10]), -5);
        assert_eq!(solve_part1(&[1,-1]),0);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(&[1,-1]), 0);
        assert_eq!(solve_part2(&[3,3,4,-2,-4]), 10);
    }
}