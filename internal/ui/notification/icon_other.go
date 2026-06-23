//go:build !darwin

package notification

import (
	_ "embed"
)

//go:embed puppypatch-icon-solo.png
var Icon []byte
