use crate::pretty_json::Write;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Version {
    pub version: String,
    pub repo: String,
}

impl Version {
    pub fn new(version: &str, repo: &str) -> Version {
        Version {
            version: String::from(version),
            repo: String::from(repo),
        }
    }
}

impl Write for Version {}
