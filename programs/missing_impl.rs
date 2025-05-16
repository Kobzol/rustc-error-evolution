struct Person {
    name: String
}

fn main() {
    let person = Person {
        name: "Michael".to_string()
    };
    println!("{:?}", person);
}
