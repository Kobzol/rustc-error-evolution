#![allow(unused)]

struct S(u32);

fn main() {
    let s = S(0);
    let s2 = s;

    println!("{}", s.0);
}
