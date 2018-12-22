use std::collections::HashMap;
#[aoc(day2, part1)]
pub fn solve_part1(input: &str) -> usize {
    let mut twice: usize = 0;
    let mut thrice: usize = 0;
    for line in input.lines() {
        let mut chars = HashMap::new();
        for c in line.chars() {
            *chars.entry(c).or_insert(0 as usize) += 1;
        }
        if chars.values().any(|&v| v == 2 as usize) {
            twice += 1;
        }
        if chars.values().any(|&v| v == 3 as usize) {
            thrice += 1;
        }
    }
    twice * thrice
}

#[aoc(day2, part2)]
pub fn solve_part2(input: &str) -> String {
    let lines: Vec<&str> = input.lines().collect();
    for skipchar in 0..lines[0].len() {
        let  bytelines: Vec<Vec<u8>> = lines.iter().map(|&l| l.bytes().enumerate()
            .filter_map(|(i,v)| {
                if i == skipchar {
                    None
                } else {
                    Some(v)
                }
            }).collect()).collect();
        for (i,x) in bytelines.iter().enumerate() {
            for y in bytelines.iter().skip(i+1) {
                if x == y {
                    return String::from_utf8(x.clone()).unwrap()
                }
            }
        }
    }
    unreachable!()
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1("aba\naaabb"), 2);
        assert_eq!(solve_part1("aba\naaab"), 1);
        assert_eq!(solve_part1("aba\naab"), 0);

    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2("abc\nabd\nace"), "ab");
        assert_eq!(solve_part2("abcde\nabdde"), "abde")
    }
}
