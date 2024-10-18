use serde::{Deserialize, Serialize, Serializer};
use std::error::Error;
use std::fs::write;
use validator::Validate;

fn sort_alphabetically<T: Serialize, S: Serializer>(
    value: &T,
    serializer: S,
) -> Result<S::Ok, S::Error> {
    let value = serde_json::to_value(value).map_err(serde::ser::Error::custom)?;
    value.serialize(serializer)
}

#[derive(Serialize)]
struct SortAlphabetically<T: Serialize>(#[serde(serialize_with = "sort_alphabetically")] T);

pub trait Json {
    fn to_json(&self) -> Result<String, Box<dyn Error>>
    where
        Self: Serialize,
    {
        let mut buf = Vec::new();
        let formatter = serde_json::ser::PrettyFormatter::with_indent(b"    ");
        let mut ser = serde_json::Serializer::with_formatter(&mut buf, formatter);
        SortAlphabetically(self).serialize(&mut ser)?;
        let out = String::from_utf8(buf)?;
        Ok(out)
    }

    fn write(&self, path: &str) -> Result<(), Box<dyn Error>>
    where
        Self: Serialize,
    {
        let out = self.to_json()?;
        write(path, out)?;
        Ok(())
    }
}

pub fn from_str<'a, T>(s: &'a str) -> Result<T, Box<dyn Error>>
where
    T: Deserialize<'a> + Validate,
{
    let out: T = serde_json::from_str(s)?;
    out.validate()?;
    Ok(out)
}
