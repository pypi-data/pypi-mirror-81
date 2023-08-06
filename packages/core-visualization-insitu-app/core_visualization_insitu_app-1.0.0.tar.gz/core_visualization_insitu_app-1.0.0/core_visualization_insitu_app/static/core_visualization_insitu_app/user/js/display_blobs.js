var display_3d_visualization = function(){
    $.ajax({
        url: update_3d,
        type: "POST",
        dataType: 'json',
        success: function(data){
            if ( Object.keys(data).length !== 0) {load_stl_document(data.file_location_uri.toString()); }
            else { load_no_stl(); };
            hideVisuLoadingSpinner();
            },
        error: function(data){
            hideVisuLoadingSpinner();
            console.log("Error");
            }
        });
    };


var load_stl_document = function(stl_document){

    // Set up
    var container = document.createElement( 'div' );
    container.setAttribute("id", "stl-container");
    document.body.appendChild( container );
    var camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 1, 1000);
    var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize( 396, 296);
    container.appendChild( renderer.domElement );

    // User interactions
    var controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.rotateSpeed = 0.5;
    controls.enableZoom = true;
    controls.autoRotate = true;
    controls.autoRotateSpeed = .75;

    // Set up scene
    var scene = new THREE.Scene();
    scene.background = new THREE.Color( 0xd9d9d9 );
    scene.add(new THREE.AmbientLight(0xffffff, 1));

    // Lights
    addShadowedLight( 1, 1, 1, 0xd9d9d9, 0.1 );
    addShadowedLight( 0.5, 1, - 1, 0xa6a6a6, 0.3 );

    function addShadowedLight( x, y, z, color, intensity ) {
        var directionalLight = new THREE.DirectionalLight( color, intensity );
        directionalLight.position.set( x, y, z );
        scene.add( directionalLight );
        directionalLight.castShadow = true;
        var d = 1;
        directionalLight.shadow.camera.left = - d;
        directionalLight.shadow.camera.right = d;
        directionalLight.shadow.camera.top = d;
        directionalLight.shadow.camera.bottom = - d;
        directionalLight.shadow.camera.near = 1;
        directionalLight.shadow.camera.far = 4;
        directionalLight.shadow.bias = - 0.002;
    }

    // Load STL
    var material = new THREE.MeshStandardMaterial( { color: 0xb3b3b3 } );

    var loader = new THREE.STLLoader();

    loader.load( stl_document, function ( geometry ) {
       var mesh = new THREE.Mesh( geometry, material );
       scene.add( mesh );

       var edges = new THREE.EdgesGeometry( geometry );
       var line = new THREE.LineSegments( edges, new THREE.LineBasicMaterial( { color: 0x000000 } ) );
       scene.add( line );

        // Place the model
        var middle = new THREE.Vector3();
        geometry.computeBoundingBox();
        geometry.boundingBox.getCenter(middle);

        mesh.position.x = -1 * middle.x;
        mesh.position.y = -1 * middle.y;
        mesh.position.z = -1 * middle.z;

        line.position.x = -1 * middle.x;
        line.position.y = -1 * middle.y;
        line.position.z = -1 * middle.z;

        // Pull the camera away
        var largestDimension = Math.max(geometry.boundingBox.max.x, geometry.boundingBox.max.y, geometry.boundingBox.max.z);
        camera.position.z = largestDimension * 1.5;

        animate();
        });

    // Axes

    // renderer
    container2 = document.createElement('div');
    container2.setAttribute("id", "stl-inset");
    document.body.appendChild( container2 );

    renderer2 = new THREE.WebGLRenderer();
    renderer2.setClearColor( 0xf0f0f0, 1 );
    renderer2.setSize( 78, 78 );
    container2.appendChild( renderer2.domElement );

    // scene
    scene2 = new THREE.Scene();

    // camera
    camera2 = new THREE.PerspectiveCamera( 50, 1, 1, 1000 );
    camera2.up = camera.up; // important!

    // axes
    axes = new THREE.AxisHelper( 150 );
    var position = axes.geometry.attributes.position;

    // Add labels
    scene2.add( axes);

    // Animate callback function
    var animate = function () {
        requestAnimationFrame(animate);
        controls.update();

        camera2.position.copy( camera.position );
        camera2.position.sub( controls.target ); // added by @libe
        camera2.position.setLength( 300 );

        camera2.lookAt( scene2.position );
        render();
    };

    var render = function () {
        renderer.render( scene, camera );
        renderer2.render( scene2, camera2 );
    };

    // Axes label Y (is X in lib)
    var loader = new THREE.FontLoader();
    loader.load( '/static/core_visualization_insitu_app/user/libs/helvetiker_regular.typeface.json', function ( font ) {
        textGeo = new THREE.TextGeometry( 'Y', {
        font: font,
        size: 30,
            height: 15,
        curveSegments: 10,
        } );

    var  color = new THREE.Color();
    color.setRGB(255, 0, 0);
    textMaterial = new THREE.MeshBasicMaterial({ color: color });
    meshText = new THREE.Mesh(textGeo, textMaterial);

    // Position of axis
    var labelY = position.getX(0);
    meshText.position.x = labelY + 70
    meshText.position.y = 5;
    meshText.position.z = 0;

    meshText.rotation = camera2.rotation;
    scene2.add(meshText);

    });

     // Axes label Z (is Y in lib)
    var loader = new THREE.FontLoader();
    loader.load( '/static/core_visualization_insitu_app/user/libs/helvetiker_regular.typeface.json', function ( font ) {
        textGeo = new THREE.TextGeometry( 'Z', {
        font: font,
        size: 30,
            height: 15,
        curveSegments: 10,
        } );

    var  color = new THREE.Color();
    color.setRGB(0, 255, 0);
    textMaterial = new THREE.MeshBasicMaterial({ color: color });
    meshText = new THREE.Mesh(textGeo, textMaterial);

    // Position of axis
    var labelZ = position.getY(0);
    meshText.position.x = 5;
    meshText.position.y = labelZ + 70;
    meshText.position.z = 0;

    meshText.rotation = camera2.rotation;
    scene2.add(meshText);

    });

    // Axes label X (is Z in lib)
    var loader = new THREE.FontLoader();
    loader.load( '/static/core_visualization_insitu_app/user/libs/helvetiker_regular.typeface.json', function ( font ) {
        textGeo = new THREE.TextGeometry( 'X', {
        font: font,
        size: 30,
            height: 15,
        curveSegments: 10,
        } );

    var  color = new THREE.Color();
    color.setRGB(0, 0, 255);
    textMaterial = new THREE.MeshBasicMaterial({ color: color });
    meshText = new THREE.Mesh(textGeo, textMaterial);

    // Position of axis
    var labelX = position.getZ(0);
    meshText.position.x = 0;
    meshText.position.y = 5;
    meshText.position.z = labelX + 70;

    meshText.rotation = camera2.rotation;
    scene2.add(meshText);

    });

    document.getElementById("stl-document").innerHTML = '';
    document.getElementById("stl-document").appendChild(container);
    document.getElementById("stl-document").appendChild(container2);
}

var load_no_stl = function(){
    document.getElementById("stl-document").innerHTML = "<img src=\"/static/core_visualization_insitu_app/user/img/no_data_400x300.jpg\" alt=\"No STL Document\">";

}