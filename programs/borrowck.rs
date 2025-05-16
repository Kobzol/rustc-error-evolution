#![allow(unused)]

fn main() {
    let mut a = 5;
    let b = &mut a;
    let x = &a;
    println!("{}", b);
}
