use regex::Regex;

#[derive(PartialEq, Debug)]
pub struct Label {
    package: String,
    target: String,
}

impl Label {
    fn new(package: &str, target: &str) -> Label {
        Label {
            package: String::from(package),
            target: String::from(target),
        }
    }

    pub fn package(&self) -> &str {
        &self.package
    }

    pub fn target(&self) -> &str {
        &self.target
    }

    pub fn canonicalise(label: &str, current_package: &str) -> Result<Label, String> {
        if label.is_empty() && current_package.is_empty() {
            return Err(String::from("Label or current package must be specified"));
        }

        let re =
            Regex::new(r"^((?P<absolute>//)(?P<package>[^:]*))?:?(?P<target>[^:]+)?$").unwrap();
        let captures = match re.captures(label) {
            Some(captures) => captures,
            None => {
                return Err(format!("Invalid label '{}'", label));
            }
        };

        let absolute = captures.name("absolute").is_some();
        let mut package = captures.name("package").map_or("", |m| m.as_str());
        let mut target = captures.name("target").map_or("", |m| m.as_str());
        Self::validate_package(current_package)?;
        Self::validate_package(package)?;
        Self::validate_target(target)?;

        if package.is_empty() && target.is_empty() {
            return Err(String::from("Either package or target must be specified"));
        }
        if !package.is_empty() && target.is_empty() {
            target = package.split("/").last().expect("Should never happen");
        }
        if !target.is_empty() && package.is_empty() && !absolute {
            package = current_package;
        }

        Ok(Label::new(package, target))
    }

    fn validate_package(package: &str) -> Result<(), String> {
        fn valid(c: char) -> bool {
            c.is_ascii_alphanumeric() || "/-.@_".contains(c)
        }

        for c in package.chars() {
            if !valid(c) {
                return Err(format!("Invalid character '{}' in package: {}", c, package));
            }
        }

        if package.starts_with('/') {
            return Err(format!("Packages must not start with a '/': {}", package));
        }
        if package.ends_with('/') {
            return Err(format!("Packages must not end with a '/': {}", package));
        }
        if package.contains("//") {
            return Err(format!("Packages must not contain '//': {}", package));
        }

        Ok(())
    }

    fn validate_target(target: &str) -> Result<(), String> {
        fn valid(c: char) -> bool {
            // We deliberately exclude closing parenthesis from this list, even
            // though it's valid according to the bazel spec, because it messes
            // up markdown image handling.
            c.is_ascii_alphanumeric() || "%-@^_\"#$&'(*-+,;<=>?[]{|}~/.".contains(c)
        }

        for c in target.chars() {
            if !valid(c) {
                return Err(format!("Invalid character '{}' in target: {}", c, target));
            }
        }

        if target.starts_with('/') {
            return Err(format!("Targets must not start with a '/': {}", target));
        }
        if target.ends_with('/') {
            return Err(format!("Targets must not end with a '/': {}", target));
        }
        if target.contains("//") {
            return Err(format!("Targets must not contain '//': {}", target));
        }
        if target.split('/').any(|i| i == "..") {
            return Err(format!(
                "Targets must not contain up-level references '..': {}",
                target
            ));
        }
        if target.split('/').any(|i| i == ".") {
            return Err(format!(
                "Targets must not contain current-directory references '.': {}",
                target
            ));
        }

        Ok(())
    }
}

#[cfg(test)]
mod label_test {
    use super::Label;

    #[test]
    fn test_validate_package() {
        assert!(Label::validate_package("").is_ok());
        assert!(Label::validate_package("a").is_ok());
        assert!(Label::validate_package("abc/DEF123-.@_").is_ok());

        assert!(Label::validate_package("!").is_err());
        assert!(Label::validate_package("/a").is_err());
        assert!(Label::validate_package("a/").is_err());
        assert!(Label::validate_package("a//b").is_err());
    }

    #[test]
    fn test_validate_target() {
        assert!(Label::validate_target("").is_ok());
        assert!(Label::validate_target("a").is_ok());
        assert!(Label::validate_target("abc/DEF123%-@^_\"#$&'(*-+,;<=>?[]{|}~/.a").is_ok());

        assert!(Label::validate_target("!").is_err());
        assert!(Label::validate_target("/a").is_err());
        assert!(Label::validate_target("a/").is_err());
        assert!(Label::validate_target("a//b").is_err());
        assert!(Label::validate_target("a/../b").is_err());
        assert!(Label::validate_target("a/./b").is_err());
    }

    #[test]
    fn test_canonicalise() {
        assert!(Label::canonicalise("", "").is_err());
        assert!(Label::canonicalise("", "a").is_err());
        assert!(Label::canonicalise("/", "a").is_err());
        assert!(Label::canonicalise("//", "a").is_err());
        assert!(Label::canonicalise("//:", "a").is_err());
        assert!(Label::canonicalise(":", "a").is_err());
        assert!(Label::canonicalise("a:", "a").is_err());
        assert!(Label::canonicalise("a/", "a").is_err());
        assert!(Label::canonicalise("/a", "a").is_err());
        assert!(Label::canonicalise("//a:b:c", "a").is_err());
        assert!(Label::canonicalise("!", "a").is_err());

        assert_eq!(
            Label::canonicalise("//a", "z").unwrap(),
            Label::new("a", "a"),
        );
        assert_eq!(
            Label::canonicalise("//a/b", "z").unwrap(),
            Label::new("a/b", "b"),
        );
        assert_eq!(
            Label::canonicalise("//a:", "z").unwrap(),
            Label::new("a", "a"),
        );
        assert_eq!(
            Label::canonicalise("//a:b", "z").unwrap(),
            Label::new("a", "b"),
        );
        assert_eq!(
            Label::canonicalise("//a/b:c/d", "z").unwrap(),
            Label::new("a/b", "c/d"),
        );
        assert_eq!(
            Label::canonicalise("//:a", "z").unwrap(),
            Label::new("", "a"),
        );
        assert_eq!(
            Label::canonicalise("//:a/b", "z").unwrap(),
            Label::new("", "a/b"),
        );
        assert_eq!(
            Label::canonicalise(":a/b", "z").unwrap(),
            Label::new("z", "a/b"),
        );
        assert_eq!(
            Label::canonicalise("a/b", "z").unwrap(),
            Label::new("z", "a/b"),
        );
        assert_eq!(Label::canonicalise("a", "").unwrap(), Label::new("", "a"),);
    }
}
