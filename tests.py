import asyncio
from uuid import UUID

from vision_client import VisionClient
from vision_client.models import (
    Cookie,
    Fingerprint,
    FolderColors,
    FolderIcons,
    Geolocation,
    InstantBehavior,
    InstantStartBody,
    OSType,
    ProxyCreateItem,
    ProxyType,
    SmartMode,
    StatusColors,
    TagColors,
)

TOKEN = ''


# ---------- вывод ----------

def section(title: str) -> None:
    bar = '=' * 60
    print(f'\n{bar}\n  {title}\n{bar}')


def step(title: str) -> None:
    print(f'\n-- {title}')


def row(*parts: object) -> None:
    print('   ' + ', '.join(str(p) for p in parts))


def sub(*parts: object) -> None:
    print('     ' + ', '.join(str(p) for p in parts))


# ---------- утилиты ----------

async def mk_folder(client: VisionClient, name: str) -> UUID:
    folder = await client.create_folder(
        folder_name=name,
        folder_icon=FolderIcons.Google,
        folder_color=FolderColors.GRAY,
    )
    return folder.id


async def mk_fingerprint(client: VisionClient) -> Fingerprint:
    fp = await client.get_fingerprint(OSType.WINDOWS)
    fp.webrtc_pref = 'auto'
    fp.canvas_pref = 'real'
    fp.webgl_pref = 'real'
    fp.ports_protection = [3389, 5900, 5901, 5800, 7070, 6568, 5938, 1080, 8080, 3128, 3030]
    return fp


# ---------- тесты ----------

async def test_folders(client: VisionClient) -> None:
    section('FOLDERS')

    step('get_folders')
    folders = await client.get_folders()
    row(f'total={len(folders)}')

    step('create_folder')
    created = await client.create_folder(
        folder_name='test-folder',
        folder_icon=FolderIcons.Google,
        folder_color=FolderColors.BLUE,
    )
    folder_id = created.id
    row(f'id={folder_id}', f'name={created.folder_name}')
    row(f'icon={created.folder_icon}', f'color={created.folder_color}')

    step('edit_folder (rename + recolor)')
    edited = await client.edit_folder(
        folder_id=folder_id,
        folder_name='test-folder-renamed',
        folder_color=FolderColors.GREEN,
    )
    row(f'name={edited.folder_name}', f'color={edited.folder_color}')

    step('delete_folder')
    deleted = await client.delete_folder(folder_id)
    row(f'deleted_profiles={len(deleted.data)}')
    row(f'usage: users={deleted.usage.users}', f'profiles={deleted.usage.profiles}')


async def test_tags(client: VisionClient) -> None:
    section('TAGS')

    folder_id = await mk_folder(client, 'test-tags-folder')
    row(f'folder_id={folder_id}')

    step('get_tags (пустой)')
    empty = await client.get_tags(folder_id)
    row(f'total={len(empty)}')

    step('create_tags (строка + пара с цветом)')
    created = await client.create_tags(
        folder_id,
        tags=[
            'plain-tag',
            ('colored-tag', TagColors.PINK),
        ],
    )
    row(f'total={len(created)}')
    for t in created:
        sub(f'id={t.id}', f'name={t.tag_name}', f'color={t.color}')

    step('get_tags (после создания)')
    listed = await client.get_tags(folder_id)
    row(f'total={len(listed)}')

    step('edit_tag (rename + recolor)')
    target = created[0]
    edited = await client.edit_tag(
        folder_id=folder_id,
        tag_id=target.id,
        name='plain-tag-renamed',
        color=TagColors.BLUE,
    )
    row(f'name={edited.tag_name}', f'color={edited.color}')

    step('delete_tags (один)')
    deleted = await client.delete_tags(folder_id, tag_ids=[target.id])
    row(f'deleted={len(deleted)}')

    step('delete_folder')
    await client.delete_folder(folder_id)


async def test_statuses(client: VisionClient) -> None:
    section('STATUSES')

    folder_id = await mk_folder(client, 'test-statuses-folder')
    row(f'folder_id={folder_id}')

    step('get_statuses (пустой)')
    empty = await client.get_statuses(folder_id)
    row(f'total={len(empty)}')

    step('create_statuses')
    created = await client.create_statuses(
        folder_id,
        statuses=[
            ('Good', StatusColors.GREEN),
            ('Bad', StatusColors.RED),
        ],
    )
    row(f'total={len(created)}')
    for s in created:
        sub(f'id={s.id}', f'status={s.status}', f'color={s.status_color}')

    step('get_statuses (после создания)')
    listed = await client.get_statuses(folder_id)
    row(f'total={len(listed)}')
    for s in listed:
        sub(f'status={s.status}', f'profiles={s.profiles}')

    step('edit_status (rename + recolor)')
    target = created[0]
    edited = await client.edit_status(
        folder_id=folder_id,
        status_id=target.id,
        name='Great',
        color=StatusColors.BLUE,
    )
    row(f'status={edited.status}', f'color={edited.status_color}')

    step('delete_statuses (один)')
    deleted = await client.delete_statuses(folder_id, status_ids=[target.id])
    row(f'deleted={len(deleted)}')

    step('delete_folder')
    await client.delete_folder(folder_id)


async def test_proxies(client: VisionClient) -> None:
    section('PROXIES')

    folder_id = await mk_folder(client, 'test-proxies-folder')
    row(f'folder_id={folder_id}')

    step('get_proxies (пустой)')
    empty = await client.get_proxies(folder_id)
    row(f'total={len(empty)}')

    step('create_proxies (model + dict)')
    created = await client.create_proxies(
        folder_id,
        proxies=[
            ProxyCreateItem(
                proxy_name='model-proxy',
                proxy_type=ProxyType.SOCKS5,
                proxy_ip='1.1.1.1',
                proxy_port=1080,
            ),
            {
                'proxy_name': 'dict-proxy',
                'proxy_type': 'HTTP',
                'proxy_ip': '2.2.2.2',
                'proxy_port': 8080,
                'proxy_username': 'u',
                'proxy_password': 'p',
            },
        ],
    )
    row(f'total={len(created)}')
    for p in created:
        sub(f'id={p.id}', f'name={p.proxy_name}', f'type={p.proxy_type}', f'{p.proxy_ip}:{p.proxy_port}')

    step('get_proxies (после создания)')
    listed = await client.get_proxies(folder_id)
    row(f'total={len(listed)}')
    for p in listed:
        sub(f'name={p.proxy_name}', f'profiles={p.profiles}', f'geo={p.geo_info}')

    step('edit_proxy (полное обновление + proxy_geo)')
    target = created[0]
    edited = await client.edit_proxy(
        folder_id=folder_id,
        proxy_id=target.id,
        proxy_name='renamed',
        proxy_type=ProxyType.HTTPS,
        proxy_ip='9.9.9.9',
        proxy_port=9999,
        update_url='https://example.com/upd',
        proxy_geo=Geolocation(
            ip='8.8.8.8',
            country='US',
            city='NY',
            timezone='America/New_York',
            latitude=40.7,
            longitude=-74.0,
        ),
    )
    row(f'name={edited.proxy_name}', f'type={edited.proxy_type}', f'{edited.proxy_ip}:{edited.proxy_port}')
    row(f'update_url={edited.update_url}', f'geo_info={edited.geo_info}')

    step('delete_proxies (один)')
    deleted = await client.delete_proxies(folder_id, proxy_ids=[target.id])
    row(f'deleted={len(deleted)}')

    step('delete_folder')
    await client.delete_folder(folder_id)


async def test_profiles(client: VisionClient) -> None:
    section('PROFILES')

    folder_id = await mk_folder(client, 'test-profiles-folder')
    row(f'folder_id={folder_id}')

    step('get_profiles (пустой)')
    empty = await client.get_profiles(folder_id)
    row(f'total={empty.total}', f'items={len(empty.items)}')

    step('get_fingerprint + настройка pref')
    fp = await mk_fingerprint(client)
    row(f'major={fp.major}', f'crc={fp.crc}')

    step('create_profile')
    created = await client.create_profile(
        folder_id,
        profile_name='test-profile',
        fingerprint=fp,
        profile_notes='сгенерированный тестовый профиль',
        new_profile_tags=['auto-tag'],
    )
    profile_id = created.data.id

    row(f'id={profile_id}', f'name={created.data.profile_name}')
    row(f'browser={created.data.browser}', f'platform={created.data.platform}')
    row(f'fp.major={created.data.fingerprint.major}', f'webrtc_pref={created.data.fingerprint.webrtc_pref}')

    step('get_profiles (после создания)')
    listed = await client.get_profiles(folder_id)
    row(f'total={listed.total}')
    for p in listed.items:
        sub(f'name={p.profile_name}', f'major={p.major}', f'running={p.running}', f'tags={p.profile_tags}')

    step('get_profile')
    got = await client.get_profile(folder_id, profile_id)
    row(f'name={got.profile_name}', f'fp.crc={got.fingerprint.crc}')

    step('edit_profile (rename + pin + new_tag)')
    edited = await client.edit_profile(
        folder_id=folder_id,
        profile_id=profile_id,
        profile_name='test-profile-renamed',
        pinned=True,
        new_profile_tags=['auto-tag-2'],
    )
    row(f'name={edited.profile_name}', f'pinned={edited.pinned}', f'tags={edited.profile_tags}')

    step('delete_profile')
    deleted = await client.delete_profile(folder_id, profile_id)
    row(f'deleted_id={deleted.data}')

    step('delete_folder')
    await client.delete_folder(folder_id)


async def test_cookies(client: VisionClient) -> None:
    section('COOKIES')

    folder_id = await mk_folder(client, 'test-cookies-folder')
    fp = await mk_fingerprint(client)
    profile = await client.create_profile(folder_id, profile_name='ck-profile', fingerprint=fp)
    profile_id = profile.data.id
    row(f'folder_id={folder_id}', f'profile_id={profile_id}')

    step('get_cookies (пустой)')
    empty = await client.get_cookies(folder_id, profile_id)
    row(f'total={len(empty)}')

    step('import_cookies (model + dict)')
    imp = await client.import_cookies(
        folder_id,
        profile_id,
        cookies=[
            Cookie(name='datr', value='abc', path='/', domain='.facebook.com', expires=1739638509),
            {
                'name': 'OTZ',
                'value': 'xyz',
                'path': '/',
                'domain': 'accounts.google.com',
                'expires': 1707670639,
            },
        ],
    )
    row(f'import={imp}')

    step('get_cookies (после import)')
    got = await client.get_cookies(folder_id, profile_id)
    row(f'total={len(got)}')
    for ck in got:
        sub(f'name={ck.name}', f'domain={ck.domain}', f'secure={ck.secure}', f'same_site={ck.same_site}')

    step('delete_folder (каскадом)')
    await client.delete_folder(folder_id)


async def test_fingerprints(client: VisionClient) -> None:
    section('FINGERPRINTS')

    step('get_fingerprint(WINDOWS)')
    fp = await client.get_fingerprint(OSType.WINDOWS)
    row(f'major={fp.major}', f'os={fp.os}', f'crc={fp.crc}')
    row(f'renderer={fp.webgl.unmasked_renderer}')

    step('get_fingerprint(MACOS, mode=ENHANCED)')
    fp_mac = await client.get_fingerprint(OSType.MACOS, mode=SmartMode.ENHANCED)
    row(f'major={fp_mac.major}', f'crc={fp_mac.crc}')

    step('get_languages')
    langs = await client.get_languages()
    row(f'total={len(langs)}', f'sample={langs[:3]}')

    step('get_timezones')
    tzs = await client.get_timezones()
    row(f'total={len(tzs)}', f'sample={tzs[:3]}')

    step('get_renderers(WINDOWS)')
    renderers = await client.get_renderers(OSType.WINDOWS)
    row(f'total={len(renderers)}', f'sample={renderers[:2]}')


async def test_local(client: VisionClient) -> None:
    section('LOCAL')

    step('get_active_profiles')
    active = await client.get_active_profiles()
    row(f'active={len(active.profiles)}')
    for p in active.profiles:
        sub(f'profile={p.profile_id}', f'folder={p.folder_id}', f'pid={p.pid}', f'port={p.port}')


async def test_instant(client: VisionClient) -> None:
    section('INSTANT')

    step('start_instant_profile() — GET без параметров')
    started = await client.start_instant_profile()
    row(f'profile_id={started.profile_id}', f'port={started.port}')

    step('stop_instant_profile')
    stopped = await client.stop_instant_profile(started.profile_id)
    row(f'cookies={len(stopped.cookies)}')

    step('start_instant_profile(InstantStartBody) — типизированный')
    body = InstantStartBody(
        name='typed-model-test',
        behavior=InstantBehavior(headless=False),
    )
    started2 = await client.start_instant_profile(body)
    row(f'profile_id={started2.profile_id}', f'port={started2.port}')

    step('stop_instant_profile')
    stopped2 = await client.stop_instant_profile(started2.profile_id)
    row(f'cookies={len(stopped2.cookies)}')

    step('start_instant_profile(dict) — сырой словарь')
    started3 = await client.start_instant_profile({'name': 'dict-test'})
    row(f'profile_id={started3.profile_id}', f'port={started3.port}')

    step('stop_instant_profile')
    stopped3 = await client.stop_instant_profile(started3.profile_id)
    row(f'cookies={len(stopped3.cookies)}')


# ---------- запуск ----------

async def main() -> None:
    async with VisionClient(x_token=TOKEN) as client:
        await test_folders(client)
        await test_tags(client)
        await test_statuses(client)
        await test_proxies(client)
        await test_profiles(client)
        await test_cookies(client)
        await test_fingerprints(client)
        await test_local(client)
        await test_instant(client)
        pass


if __name__ == '__main__':
    asyncio.run(main())