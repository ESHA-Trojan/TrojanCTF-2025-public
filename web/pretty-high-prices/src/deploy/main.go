package main

import (
	"github.com/ctfer-io/chall-manager/sdk"
	k8s "github.com/ctfer-io/chall-manager/sdk/kubernetes"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
	sdk.Run(func(req *sdk.Request, resp *sdk.Response, opts ...pulumi.ResourceOption) error {
		cm, err := k8s.NewExposedMonopod(req.Ctx, "chal1-whitehats", &k8s.ExposedMonopodArgs{
			Identity: pulumi.String(req.Config.Identity),
			Hostname: pulumi.String("isolated.trojanc.tf"),
			Container: k8s.ContainerArgs{
				Image: pulumi.String("isolatedchallengesv4registry.azurecr.io/web/chal1-whitehats:latest"),
				Ports: k8s.PortBindingArray{
					k8s.PortBindingArgs{
						Port:       pulumi.Int(80),
						ExposeType: k8s.ExposeIngress,
					},
				},
			},
			// The following fits for a Traefik-based use case
			IngressAnnotations: pulumi.ToStringMap(map[string]string{
				"traefik.ingress.kubernetes.io/router.entrypoints": "websecure",
				"traefik.ingress.kubernetes.io/router.tls":         "true",
			}),
			IngressNamespace: pulumi.String("networking"),
			IngressLabels: pulumi.ToStringMap(map[string]string{
				"app": "traefik",
			}),
		}, opts...)
		if err != nil {
			return err
		}

		resp.ConnectionInfo = pulumi.Sprintf("https://%s", cm.URLs.MapIndex(pulumi.String("80/TCP")))
		return nil
	})
}
