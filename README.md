# Rustc error evolution
This repository contains a Python script that downloads stable Rust compiler releases all the way back to 1.0, runs each compiler version on each Rust program in the `programs` directory and gathers the standard error output. The output is then outputted to a file called `errors.json`.

You can find the accompanying blog post [here](https://kobzol.github.io/rust/rustc/2025/05/16/evolution-of-rustc-errors.html).

You can then start any HTTP server (e.g. `python3 -m http.server`) and see a simple website that shows how the errors evolved over time.

Note that the `errors.json` file is pregenerated in this repository, so you can just start the server without regenerating it.

**Warning**: Downloading all Rust stable versions takes some time, and will take 50+ GiB of disk space.

## Usage

```bash
# If you want to regenerate the data (might take a long time!)
$ python3 evolution.py
$ python3 -m http.server
```

## License
[MIT](LICENSE)
