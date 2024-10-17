use serde::{Deserialize, Serialize, Serializer};
use std::error::Error;
use std::fs::write;

fn sort_alphabetically<T: Serialize, S: Serializer>(
    value: &T,
    serializer: S,
) -> Result<S::Ok, S::Error> {
    let value = serde_json::to_value(value).map_err(serde::ser::Error::custom)?;
    value.serialize(serializer)
}

#[derive(Serialize)]
struct SortAlphabetically<T: Serialize>(#[serde(serialize_with = "sort_alphabetically")] T);

pub trait Write {
    fn write(&self, path: &str) -> Result<(), Box<dyn Error>>
    where
        Self: Serialize,
    {
        let mut buf = Vec::new();
        let formatter = serde_json::ser::PrettyFormatter::with_indent(b"    ");
        let mut ser = serde_json::Serializer::with_formatter(&mut buf, formatter);
        SortAlphabetically(self).serialize(&mut ser)?;
        let data = String::from_utf8(buf)?;

        write(path, data)?;
        Ok(())
    }
}

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
