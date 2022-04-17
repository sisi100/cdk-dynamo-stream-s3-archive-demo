make-dia:
	cdk synth
	npx cdk-dia --target-path docs/diagram.png
