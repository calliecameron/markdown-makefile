use clap::{Args, Parser};
use markdown::metadata::Version;
use markdown::pretty_json::Write;
use std::error::Error;
use std::fs::read_to_string;
use std::io;

const REPO_KEY: &str = "STABLE_WORKSPACE_PARENT_REPO";
const VERSION_KEY: &str = "STABLE_WORKSPACE_PARENT_VERSION";

#[derive(Parser)]
#[command(version, about, long_about = None)]
struct Cli {
    out_file: String,
    #[command(flatten)]
    in_file: InFile,
}

#[derive(Args)]
#[group(required = true, multiple = false)]
struct InFile {
    #[arg(long = "version_file")]
    version_file: Option<String>,
    #[arg(long = "info_file")]
    info_file: Option<String>,
}

fn from_version_file(path: &str) -> io::Result<Version> {
    let data = read_to_string(path)?;
    let version: Version = serde_json::from_str(&data)?;
    Ok(version)
}

fn from_info_file(path: &str) -> io::Result<Version> {
    let mut version = None;
    let mut repo = None;

    let data = read_to_string(path)?;
    for line in data.lines() {
        if let Some(line) = line.strip_prefix(REPO_KEY) {
            repo = Some(line.trim());
        } else if let Some(line) = line.strip_prefix(VERSION_KEY) {
            version = Some(line.trim())
        }
    }

    if let (Some(version), Some(repo)) = (version, repo) {
        return Ok(Version::new(version, repo));
    }

    Ok(Version::new("unversioned", "unversioned"))
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Cli::parse();

    let version = if let Some(path) = args.in_file.version_file {
        from_version_file(&path)?
    } else if let Some(path) = args.in_file.info_file {
        from_info_file(&path)?
    } else {
        return Err("Neither version file specified".into());
    };

    version.write(&args.out_file)
}
