package logo
import ("strings";"charm.land/lipgloss/v2";"github.com/puppypatch/puppypatch/internal/ui/styles")
type Opts struct{FieldColor any;TitleColorA any;TitleColorB any;CharmColor any;VersionColor any;Width int;Hyper bool}
const asciiLogo = `█▀█ █░█ █▀█ █▀█ █▄█ █▀█ ▄▀█ ▀█▀ █▀▀ █░█
█▀▀ █▄█ █▀▀ █▀▀ ░█░ █▀▀ █▀█ ░█░ █▄▄ █▀█`
func Render(base lipgloss.Style, ver string, compact bool, o Opts) string {if compact{return "PUPPYPATCH"}; res := asciiLogo; if o.Width > 42{res+="\n"+strings.Repeat(" ",(o.Width-10)/2)+"v"+ver+"\n"}; return res}
func SmallRender(t *styles.Styles, width int, o Opts) string {return " PUPPYPATCH "+strings.Repeat("╱",max(0,width-14))}
func max(a,b int)int{if a>b{return a};return b}
