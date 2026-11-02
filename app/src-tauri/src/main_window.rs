//! The configured main webview, never an arbitrary first/focused replacement.
use tauri::{Manager, Runtime};

pub(crate) fn original<R: Runtime>(app: &tauri::AppHandle<R>) -> Option<tauri::Window<R>> {
    app.get_webview_window("main")
        .map(|window| window.as_ref().window().clone())
}

#[cfg(test)]
mod tests {
    use super::*;
    use tauri::{test::mock_app, WebviewUrl, WebviewWindowBuilder};

    #[test]
    fn configured_main_is_selected_with_auxiliary_windows_in_either_order() {
        for labels in [["auxiliary", "main"], ["main", "auxiliary"]] {
            let app = mock_app();
            for label in labels {
                WebviewWindowBuilder::new(&app, label, WebviewUrl::App("index.html".into()))
                    .build().unwrap();
            }
            assert_eq!(original(app.handle()).unwrap().label(), "main");
        }
    }

    #[test]
    fn missing_main_never_substitutes_an_auxiliary_webview() {
        let app = mock_app();
        WebviewWindowBuilder::new(&app, "auxiliary", WebviewUrl::App("index.html".into()))
            .build().unwrap();
        assert!(original(app.handle()).is_none());
    }
}
