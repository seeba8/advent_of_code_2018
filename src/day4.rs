use std::collections::BTreeMap;
use std::collections::HashMap;
use regex::Regex;
use chrono::prelude::*;

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
pub enum Status {
    Begin,
    Sleep,
    WakeUp
}
#[derive(Debug, PartialEq, Eq, Copy, Clone)]
pub struct LogEntry {
    guard: Option<usize>,
    status: Status
}

#[aoc_generator(day4)]
pub fn input_generator(input: &str) -> BTreeMap<DateTime<Utc>, LogEntry> {
    let re = Regex::new(r"\[(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})\]\s(falls asleep|wakes up|Guard #(\d+) begins shift)").expect("regex failed");
    let mut logfile: BTreeMap<DateTime<Utc>, LogEntry> = BTreeMap::new();
    for line in input.lines() {
        let caps = match re.captures(line) {
            None => continue,
            Some(x) => x
        };
        logfile.insert(Utc.datetime_from_str(&caps[1],"%Y-%m-%d %H:%M").expect(&caps[1]), {
            if caps[2].starts_with("Guard") {
                LogEntry{ guard: Some(caps[3].parse().expect(&caps[3])), status: Status::Begin }
            } else if caps[2].starts_with("falls") {
                LogEntry {guard: None, status: Status::Sleep}
            } else {
                LogEntry {guard: None, status: Status::WakeUp}
            }
        });
    }
    let mut most_recent_guard: Option<usize> = None;
    for (_, logentry) in logfile.iter_mut() {
        match logentry.status {
            Status::Begin => {
                most_recent_guard = logentry.guard;
            }
            _ => {
                logentry.guard = most_recent_guard;
            }
        };
    }
    logfile
}

#[aoc(day4, part1)]
pub fn solve_part1(input: &BTreeMap<DateTime<Utc>, LogEntry>) -> usize {
    let mut sleepminutes: HashMap<usize, usize> = HashMap::new();
    let mut startsleep: usize = 0;
    let mut slept_on_minute: HashMap<usize, [u8;60]> = HashMap::new();
    for (&time, &entry) in input {
        match entry.status {
            Status::Begin => {
                sleepminutes.entry(entry.guard.unwrap()).or_insert(0);
                slept_on_minute.entry(entry.guard.unwrap()).or_insert([0u8;60]);
            },
            Status::Sleep => {
                startsleep = time.minute() as usize;
            },
            Status::WakeUp => {
                sleepminutes.entry(entry.guard.unwrap()).and_modify(|e| {*e += time.minute() as usize - startsleep;});
                for i in startsleep..time.minute() as usize {
                    slept_on_minute.entry(entry.guard.unwrap()).and_modify(|e| {e[i] += 1u8});
                }
                startsleep = 0;
            }
        };
    }
    let mut longest_sleeper: usize = 0;
    let mut longest_sleep: usize = 0;
    for (&id, &minutes) in sleepminutes.iter() {
        if minutes > longest_sleep{
            longest_sleeper = id.clone();
            longest_sleep = minutes;
        }
    };
    let mut longest_minute = 0usize;
    let plan = slept_on_minute.get(&longest_sleeper).unwrap();
    for i in 0..60 {
        if plan[i] > plan[longest_minute] {
            longest_minute = i;
        }
    }
    longest_minute * longest_sleeper
}


#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_inputparse() {
        let mut logfile: BTreeMap<DateTime<Utc>, LogEntry> = BTreeMap::new();
        logfile.insert(Utc.datetime_from_str("1518-11-01 00:00","%Y-%m-%d %H:%M").unwrap(),
            LogEntry { guard: Some(10), status: Status::Begin}
        );
        assert_eq!(input_generator("[1518-11-01 00:00] Guard #10 begins shift"), logfile);

        let mut logfile: BTreeMap<DateTime<Utc>, LogEntry> = BTreeMap::new();
        logfile.insert(Utc.datetime_from_str("1518-05-27 00:42","%Y-%m-%d %H:%M").unwrap(),
                       LogEntry { guard: None, status: Status::Sleep});
        logfile.insert(Utc.datetime_from_str("1518-09-22 00:10","%Y-%m-%d %H:%M").unwrap(),
                       LogEntry { guard: None, status: Status::Sleep});

        logfile.insert(Utc.datetime_from_str("1518-07-14 00:53","%Y-%m-%d %H:%M").unwrap(),
                       LogEntry { guard: None, status: Status::Sleep});

        assert_eq!(input_generator("[1518-09-22 00:10] falls asleep\n[1518-05-27 00:42] falls asleep\n[1518-07-14 00:53] falls asleep"), logfile);
    }

    #[test]
    fn test_guardpropagation() {
        let mut logfile: BTreeMap<DateTime<Utc>, LogEntry> = BTreeMap::new();
        logfile.insert(Utc.datetime_from_str("1518-05-27 00:42","%Y-%m-%d %H:%M").unwrap(),
                       LogEntry { guard: None, status: Status::Sleep});
        logfile.insert(Utc.datetime_from_str("1518-09-22 00:10","%Y-%m-%d %H:%M").unwrap(),
                       LogEntry { guard: Some(2), status: Status::Sleep});

        logfile.insert(Utc.datetime_from_str("1518-07-14 00:53","%Y-%m-%d %H:%M").unwrap(),
                       LogEntry { guard: Some(2), status: Status::Begin});
        assert_eq!(input_generator("[1518-09-22 00:10] falls asleep\n[1518-05-27 00:42] falls asleep\n[1518-07-14 00:53] Guard #2 begins shift"), logfile);
    }
}