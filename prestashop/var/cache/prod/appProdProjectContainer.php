<?php

// This file has been auto-generated by the Symfony Dependency Injection Component for internal use.

if (\class_exists(\ContainerRxf9vze\appProdProjectContainer::class, false)) {
    // no-op
} elseif (!include __DIR__.'/ContainerRxf9vze/appProdProjectContainer.php') {
    touch(__DIR__.'/ContainerRxf9vze.legacy');

    return;
}

if (!\class_exists(appProdProjectContainer::class, false)) {
    \class_alias(\ContainerRxf9vze\appProdProjectContainer::class, appProdProjectContainer::class, false);
}

return new \ContainerRxf9vze\appProdProjectContainer([
    'container.build_hash' => 'Rxf9vze',
    'container.build_id' => 'd83d16c1',
    'container.build_time' => 1733865148,
], __DIR__.\DIRECTORY_SEPARATOR.'ContainerRxf9vze');
