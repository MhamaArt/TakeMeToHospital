const Deployer = require('ssh-deploy-release');
 
const options = {
    localPath: './',
    host: '77.47.207.42',
    username: 'mhama',
    password: 'Rossignol',
    //passphrase: '',
    port: 2512,
    // privateKeyFile: './key.rsa',
    deployPath: '/home/mhama/project'
};
 
const deployer = new Deployer(options);
deployer.deployRelease(() => {
    console.log('Deployed !')
});