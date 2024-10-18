use clap::Parser;
use markdown::json::{from_str, Json};
use markdown::metadata::InputMetadata;
use std::error::Error;
use std::fs::read_to_string;

#[derive(Parser)]
#[command(version, about, long_about = None)]
struct Cli {
    in_file: String,
    out_file: String,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Cli::parse();

    let data = read_to_string(args.in_file)?;
    let metadata: InputMetadata = from_str(&data)?;

    metadata.write(args.out_file)
}
